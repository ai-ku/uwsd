#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
from bs4 import BeautifulSoup
from collections import defaultdict as dd
from nlp_utils import find_files

inventory_path = sys.argv[1]

NONE_OF_ABOVE_SENSE = "none of the above"

def get_inventory_info():
    d = dd(dict)
    files = find_files(inventory_path, "*.xml")
    for num_processed, f in enumerate(files):
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)

        #soup = BeautifulSoup(open(f), 'xml')
        #senses = soup.findAll('sense')

        #for sense in senses:
            #onto_key = str(sense['n'])
            #sense_name = str(sense['name'])
            #mapping = sense.findAll('mappings')[0]
            #wn = mapping.findAll('wn')[0]
            #version = wn['version']
            #wn_senses = wn.text.strip()
            ##FIXME: None of above sense should be mapped to 3.0 first!
            #if sense_name == NONE_OF_ABOVE_SENSE:
                #wn_senses = "no_lexicon_sense"
                #version = "3.0"
