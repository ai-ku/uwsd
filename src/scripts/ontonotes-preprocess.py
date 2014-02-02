#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Preprocess and create a file that contains all information to be 
needed for constructing different test sets
"""

import sys
import os
from bs4 import BeautifulSoup
from collections import defaultdict as dd
from nltk.corpus.reader import BracketParseCorpusReader
from itertools import count
import gzip
from nlp_utils import find_files

if len(sys.argv) != 3:
    msg = "Usage: {} annotation_path sense_inventory_path"
    print >> sys.stderr, msg.format(sys.argv[0])

annotations_path = sys.argv[1]
inventory_path = sys.argv[2]

NONE_OF_ABOVE_SENSE = "none of the above"

# treebank has some peculiar mappings. fix dict above will convert them.
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }

def get_inventory_info():
    d = dd(dict)
    files = find_files(inventory_path, "*.xml")
    for num_processed, f in enumerate(files):
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)

        soup = BeautifulSoup(open(f), 'xml')
        senses = soup.findAll('sense')

        for sense in senses:
            onto_key = str(sense['n'])
            sense_name = str(sense['name'])
            mapping = sense.findAll('mappings')[0]
            wn = mapping.findAll('wn')[0]
            version = wn['version']
            wn_senses = wn.text.strip()
            #FIXME: None of above sense should be mapped to 3.0 first!
            if sense_name == NONE_OF_ABOVE_SENSE:
                wn_senses = "no_lexicon_sense"
                version = "3.0"
            ita = soup.findAll('ita') # inter-annotator agreement
            ita_score = "ITA_UNDEFINED"
            if len(ita) != 0:
                ita_score = ita[0]['ann_1_2_agreement']
            d[fn][onto_key] = [wn_senses, version, ita_score]
            
    print >> sys.stderr, "{} files processed".format(num_processed)
    return d

def annotation_process():
    d = get_inventory_info()
    annotated_files = find_files(annotations_path, "*.sense")
    pos_file = gzip.open('on.pos.gz', 'w')
    inst_num_dict = dd(lambda: count(1))
    for num_processed, fn in enumerate(annotated_files):
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)
        directory = os.path.dirname(fn)
        basename = os.path.basename(fn)
        reader = BracketParseCorpusReader(directory, basename.replace('.sense', '.parse'))
        fileid = reader.fileids()[0]
        sentences = dict()
        parsed_sents = reader.parsed_sents(fileid)
        for line in open(fn):
            line = line.split()
            tw = line[3]
            onto_sense = line[-1]
            sent_id, tok_id = int(line[1]), int(line[2])
            stuple = sentences.setdefault(sent_id, None)
            if stuple is None:
                sentence = parsed_sents[sent_id]
                clean_sent = []
                clean_pos = []
                for word, p in sentence.pos():
                    if p != '-NONE-':
                        if word in fix:
                            word = fix[word]
                        clean_sent.append(word)
                        clean_pos.append(p)
                sentences[sent_id] = (clean_sent, clean_pos)
            else:
                clean_sent, clean_pos = stuple
            lexicon_senses, version, ita = d[tw][onto_sense]
            w = tw.replace('-', '.') # following the convention of SemEval
            m = "{}\t{}.on.{}\t{}-{}-{}\t{}-{}\t{}\t{}\t{}\t{}\t{}"
            print m.format(w, w, inst_num_dict[tw].next(), line[0], sent_id, tok_id,
                w, onto_sense, lexicon_senses, version, ita, tok_id, " ".join(clean_sent))
            pos_file.write("{}\n".format(clean_pos))
    print >> sys.stderr, "{} files processed".format(num_processed)

annotation_process()
