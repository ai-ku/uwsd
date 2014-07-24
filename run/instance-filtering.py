#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Filter all instances which are annotated by using an inventory that is not WordNet.
This filtering is used in IMS Ontonotes Paper.
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
mapping_file = sys.argv[2]

# treebank has some peculiar mappings. fix dict above will convert them.
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }

