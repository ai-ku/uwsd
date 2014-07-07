#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

"""
Aim: WN 1.7 -> WN 3.0 -> Ontonotes Sense Definition
- index.sense (WN 3.0) is processed.
This file contains sense key and sense number. Sense number need to be known because
using these numbers we transform 3.0 to Ontonotes Sense definition.

Algorithm:

IMS senses -> WN 3.0

Assumption is that *sense numbers* are not different between different Wordnet version.
This may not be correct since according to documentation sense numbers are given
frequency of a word (the most frequent sense is #1 sense number).

Some senses exist in 1.7 but not in WordNet 3.0. We can't map this senses. So not_in_WN3 
list contains these senses/instances. Since these instances are not mapped, we cannot
evaluate the performance of the system for those instances (Precision/Recall should not
be the same).

After we find out sense number of an instance, we check ontonotes has this sense, if it has
we return Ontonotes equivalent of this sense, if not, we label this sense as 
no_lexicon_sense
"""

import sys
import os
from bs4 import BeautifulSoup
from collections import defaultdict as dd
from nlp_utils import find_files

inventory_path = sys.argv[1]
index_sense_f = sys.argv[2]

NONE_OF_ABOVE_SENSE = "none of the above"

wn_set = ['3.0', '2.0', '1.7'] # get only the Wordnet senses from Ontonotes

def get_inventory_info():
    d = dd(dict)
    files = find_files(inventory_path, "*.xml")
    for num_processed, f in enumerate(files):
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{0} files processed".format(num_processed)

        soup = BeautifulSoup(open(f), 'xml')
        senses = soup.findAll('sense')
        target_word = fn.replace('-', '.')

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

            if version in wn_set:
                wn_senses = map(str, wn_senses.split(','))
                for wn_s in wn_senses:
                    d[target_word][wn_s] = onto_key
    return d

def index_sense_process(fn=index_sense_f):
    
    """ Method processes the index.sense file """

    # hood%1:15:00:: 08641944 1 0
    d = dd(dict)
    for line in open(fn):
        line = line.split()
        sense_id = line[0]
        offset, sense_no, freq = line[1:]
        #print tw, sense_id, offset, sense_no, freq
        d[sense_id] = sense_no
    return d

onto_dict = get_inventory_info()
index_senses = index_sense_process()

ans_files = find_files('ims/on/testing-output', '*.ans')

not_in_WN3 = []
for fn in ans_files:
    for line in open(fn):
        line = line.split()
        tw = line[0]
        key = line[-1]
        if key in index_senses:
            wn_s = index_senses[key]
            if wn_s not in onto_dict[tw]:
                wn_s = 'no_lexicon_sense'
            try:
                sense = onto_dict[tw][wn_s]
            except KeyError:
                print >> sys.stderr, tw, key, wn_s
            line[-1] = "{0}-{1}".format(tw, sense)
            print ' '.join(line)
        else:
            not_in_WN3.append(key)

print >> sys.stderr, len(not_in_WN3), len(set(not_in_WN3)), set(not_in_WN3)


