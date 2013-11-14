#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nltk.corpus.reader import BracketParseCorpusReader
import sys
import gzip
from uwsd_utils import get_dataset_path
import os

dataset=sys.argv[1]

path = os.path.dirname(get_dataset_path(dataset))

sent_error = set(["Ruth K. Nelson Cullowhee , N.C .", ])

# Semeval07, senseval2, senseval3 dataset contain some tokenization convention.
# This tokenization should be fixed since our LM does not follow this convention.
# Details for Treebank tokenization: http://www.cis.upenn.edu/~treebank/tokenization.html
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }

if path is None:
    print >> sys.stderr, "Wrong dataset"
    exit(1)

fnames = "clean-sent sent pos".split()
files = map(lambda x: gzip.open("{}.{}.gz".format(dataset, x), 'w'), fnames)

def write2file(lines, files):
    for line, f in zip(lines,files):
        try:
            f.write(" ".join(line))
        except TypeError: # tree parsing error
            print >> sys.stderr, "Sentence Error: {}\nOnly new line writing".format(line)
        f.write('\n')

reader = BracketParseCorpusReader(path, '.*mrg')
for fileid in reader.fileids():
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
        write2file(lines, files)

map(lambda f: f.close(), files)
