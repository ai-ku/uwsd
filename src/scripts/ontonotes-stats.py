#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module provides various statistics about Ontonotes.

"""
import sys
import os
from bs4 import BeautifulSoup
from collections import defaultdict as dd
from nltk.corpus.reader import BracketParseCorpusReader
from itertools import count
from nlp_utils import find_files

if len(sys.argv) != 3:
    msg = "Usage: {} annotation_path sense_inventory_path"
    print >> sys.stderr, msg.format(sys.argv[0])

annotations_path = sys.argv[1]
inventory = sys.argv[2]

# treebank has some peculiar mappings. fix dict above will convert them.
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }


def get_filtered_set(is_only_wn=True, ita_threshold=.85):
    inventory_files = find_files(inventory, "*.xml")
    for num_processed, f in enumerate(inventory_files):
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)
        soup = BeautifulSoup(open(f), 'xml')
        ita = soup.findAll('ita') # inter-annotator agreement
        if len(ita) != 0:
            ita_score = float(ita[0]['ann_1_2_agreement'])
            if ita_score > ita_threshold:
                versions = [wn['version'] == '3.0' for wn in soup.findAll('wn')[:-1]]
                if all(versions):
                    print fn, versions, ita_score

def get_sense_mappings():
    
    version_dict = dd(lambda : count(0)) # keep tracking the annotation version
    word_sense_dict = dd(dict) # keep tracking words' senses' version
    inventory_files = find_files(inventory, "*.xml")
    # ITA INF below: [#ofinstance, #total_ita_score, #of word <90, #total_score_for_<90]
    ita_inf = [0, 0, 0, 0] 
    nsense = [0, 0]
    ita_less_90 = set()
    for num_processed, f in enumerate(inventory_files):
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)
        soup = BeautifulSoup(open(f), 'xml')
        senses = soup.findAll('sense')

        nsense[0] += len(senses)
        nsense[1] += 1

        for sense in senses:
            key = str(sense['n'])
            mapping = sense.findAll('mappings')[0]
            wn = mapping.findAll('wn')[0]
            version = wn['version']
            word_sense_dict[fn][key] = version
            wn_senses = wn.text.split(',') # maybe we can use it later
            version_dict[version].next()
        ita = soup.findAll('ita') # inter-annotator agreement
        if len(ita) != 0:
            ita_inf[0] += 1
            ita_score = float(ita[0]['ann_1_2_agreement'])
            ita_inf[1] += ita_score
            if ita_score < 0.9:
                ita_inf[2] += 1
                ita_inf[3] += ita_score
                ita_less_90.add(fn)

    ita_inf[1] = ita_inf[1] / ita_inf[0] # averaging.for all instance ita score
    ita_inf[3] = ita_inf[3] / ita_inf[2] # averaging.ita score for word lower than 0.9
    print >> sys.stderr, "{} files processed (total)".format(num_processed)
    print "ITA informations: {}".format(ita_inf)
    avg_sense = nsense[0] / float(nsense[1])
    print "total sense: {}, avg # of sense: {}".format(nsense[0], avg_sense)
    version_list = [(key, val.next()) for key, val in version_dict.iteritems()]
    version_list = sorted(version_list, key=lambda x: x[1], reverse=True)
    with open('ontonotes-sensefreq-inventory.tab', 'w') as f:
        for key, val in version_list:
             f.write("{}\t{}\n".format(key, val))
    return word_sense_dict, ita_less_90

def process_sense_annotation():
    
    print >> sys.stderr, "Sense Annotation processing started"

    word_sense_dict, ita_less_90 = get_sense_mappings()
    sense_freq = dd(lambda : count(0)) # sense freqs (wn3.0, wn2.0 etc) for annotation
    word_freq = dd(lambda : count(0)) # words frequency in annontation
    pos_dict = dd(lambda : count(0)) # pos distribution for annotation.
    num_adjudicated = 0 # Number of instance that adjudicated
    pattern = "*.sense"
    annotated_files = find_files(annotations_path, pattern)
    num_word_processed = 0 
    ita_less90_count = 0
    for num_processed, annotated_file in enumerate(annotated_files):
        #fn = annotated_file.replace(annotations_path, "")
        for line in open(annotated_file):
            line = line.split()
            num_word_processed += +1
            if len(line) == 6:
                num_adjudicated += 1
            word = line[3]
            pos_tag = word[-1]
            pos_dict[pos_tag].next()
            sense_tag = line[-1]
            word_freq[word].next()

            version = word_sense_dict[word][sense_tag]
            sense_freq[version].next()

            if word in ita_less_90:
                ita_less90_count += 1

        if num_processed % 3000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)

    ### Printing: Pos Info in annotated corpus  ###
    num_noun = pos_dict['n'].next()
    num_verb = pos_dict['v'].next()
    pos_msg = "Noun\tVerb\tNoun+Verb\tTotalWord\n{}\t{}\t{}\t{}"
    print pos_msg.format(num_noun, num_verb, num_verb + num_noun, num_word_processed)

    ### Printing: Number of Adjudicated word
    print "Number of adjudicated case: {}".format(num_adjudicated)

    ### Writing: sense frequency in annotated data 
    sensefreq_list = [(key, val.next()) for key, val in sense_freq.iteritems()]
    sensefreq_list = sorted(sensefreq_list, key=lambda x: x[1], reverse=True)
    with open('ontonotes-sensefreq-annotation.tab', 'w') as f:
        for key, val in sensefreq_list:
             f.write("{}\t{}\n".format(key, val))
    m = "Number of words that have <90 ita score {} in annotated data"
    print m.format(ita_less90_count)
    print >> sys.stderr, "Sense Annotation processing finished"

def process_parse_annotation():
    print >> sys.stderr, "Parsing started"
    reader = BracketParseCorpusReader(annotations_path, '.*parse')
    pos_set = set("NN VB RB JJ".split()) # word level pos tags for n, v, adv, adj.
    check_pos = lambda x: x in pos_set
    d = dd(lambda: count(0))
    for fileid in reader.fileids():
        #print fileid
        for sentence in reader.parsed_sents(fileid):
            for word, p in sentence.pos():
                pos = p[0:2]
                if p != '-NONE-' and check_pos(pos):
                     d[pos].next()
    print [(pos, c.next()) for pos, c in d.iteritems()]
    print >> sys.stderr, "Parsing finished"

def main():
    #process_parse_annotation()
    #process_sense_annotation()
    get_filtered_set()

if __name__== "__main__":
    main()
