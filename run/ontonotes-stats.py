#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module provides various statistics about Ontonotes.

"""

import sys
import os
from bs4 import BeautifulSoup
import fnmatch
from collections import defaultdict as dd
from nltk.corpus.reader import BracketParseCorpusReader
from itertools import count


ONTO_PATH = sys.argv[1]

inventory = os.path.join(ONTO_PATH, "data/files/data/english/metadata/sense-inventories/")
annotations_path = os.path.join(ONTO_PATH, "data/files/data/english/annotations")

# treebank has some peculiar mappings. fix dict above will convert them.
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }

def find_files(topdir, pattern):
    for path, dirname, filelist in os.walk(topdir):
        for name in filelist:
            if fnmatch.fnmatch(name, pattern):
                yield os.path.join(path,name)

def get_sense_mappings():
    
    d = dd(lambda : count(0))
    word_sense_dict = dd(dict)
    inventory_files = find_files(inventory, "*.xml")
    num_processed = 0
    # ITA INF below: [#ofinstance, #total_ita_score, #of word <90, #total_score_for_<90]
    ita_inf = [0, 0, 0, 0] 
    for f in inventory_files:
        num_processed += 1
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)
        soup = BeautifulSoup(open(f), 'xml')
        senses = soup.findAll('sense')

        for sense in senses:
            key = sense['n']
            mapping = sense.findAll('mappings')[0]
            wn = mapping.findAll('wn')[0]
            version = wn['version']
            word_sense_dict[fn][key] = version
            wn_senses = wn.text.split(',')
            d[version].next()
        ita = soup.findAll('ita') # inter-annotator agreement
        if len(ita) != 0:
            ita_inf[0] += 1
            ita_score = float(ita[0]['ann_1_2_agreement'])
            ita_inf[1] += ita_score
            if ita_score < 0.9:
                ita_inf[2] += 1
                ita_inf[3] += ita_score

    ita_inf[1] = ita_inf[1] / ita_inf[0] # averaging.for all instance ita score
    ita_inf[3] = ita_inf[3] / ita_inf[2] # averaging.ita score for word lower than 0.9
    print ita_inf
    print num_processed

def process_sense_annotation():
    
    print >> sys.stderr, "Sense Annotation processing started"
    
    d = dd(lambda : count(0))
    pos_dict = dd(lambda : count(0))
    num_adjudicated = 0 # Number of instance that adjudicated
    pattern = "*.sense"
    annotated_files = find_files(annotations_path, pattern)
    for annotated_file in annotated_files:
        fn = annotated_file.replace(annotations_path, "")
        for line in open(annotated_file):
            line = line.split()
            if len(line) == 6:
                num_adjudicated += 1
            word = line[3]
            pos_tag = word[-1]
            pos_dict[pos_tag].next()
            sense_tag = line[-1]
            d[word].next()
            #print fn, word, pos_tag, sense_tag
    print pos_dict['n'].next(), pos_dict['v'].next()
    exit()

    print >> sys.stderr, "Sense Annotation processing finished"

def process_parse_annotation():
    reader = BracketParseCorpusReader(annotations_path, '.*parse')
    for fileid in reader.fileids():
        print fileid
        for sentence in reader.parsed_sents(fileid):
            clean_sent_list = []
            sent_list = []
            pos_list = []
            for word, p in sentence.pos():
                if p != '-NONE-':
                    if word in fix:
                        word = fix[word]
                    clean_sent_list.append(word)
                sent_list.append(word)
                pos_list.append(p)
            lines = [clean_sent_list, sent_list, pos_list]
            print lines
        exit()
            #write2file(lines, files)
    pass
process_parse_annotation()
#get_sense_mappings()
#process_sense_annotation()
