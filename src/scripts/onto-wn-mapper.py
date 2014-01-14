#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Ontonotes - Wordnet version X Mapper.

Output format: word <tab> ontonotes_sense_number <tab> correspondent_word_net_sense_list
"""

import sys
import os
from bs4 import BeautifulSoup
from collections import defaultdict as dd
from nltk.corpus.reader import BracketParseCorpusReader
from itertools import count
from nlp_utils import find_files

if len(sys.argv) != 4:
    msg = "Usage: {} sense_inventory_path word_list_file wordnet_version"
    print >> sys.stderr, msg.format(sys.argv[0])

inventory_path = sys.argv[1]
words_file = sys.argv[2]
wn_version = sys.argv[3]

# treebank has some peculiar mappings. fix dict above will convert them.
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }
    
files = open(words_file).read().split()
for num_processed, fn in enumerate(files):
    f = os.path.join(inventory_path, fn + ".xml")
    if num_processed % 1000 == 0:
        print >> sys.stderr, "{} files processed".format(num_processed)
    soup = BeautifulSoup(open(f), 'xml')
    senses = soup.findAll('sense')

    for sense in senses:
        onto_key = str(sense['n'])
        mapping = sense.findAll('mappings')[0]
        wn = mapping.findAll('wn')[0]
        version = wn['version']
        if version == wn_version:
            print "{}\t{}\t{}".format(fn, onto_key, wn.text)
        #word_sense_dict[fn][key] = version
        #wn_senses = wn.text.split(',') # maybe we can use it later
        #version_dict[version].next()
print >> sys.stderr, "{} files processed".format(num_processed)


