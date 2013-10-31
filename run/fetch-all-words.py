#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nltk.corpus import treebank
import sys

semeval2007 = "wsj_0105.mrg  wsj_0186.mrg  wsj_0239.mrg"
senseval3 = "cl23.mrg wsj_1695.mrg wsj_1778.mrg"
senseval2 = "wsj_0089.mrg  wsj_0465.mrg  wsj_1286.mrg"

dataset = sys.argv[1]
if dataset == 'semeval2007':
    files = semeval2007
elif dataset == 'senseval3':
    files = senseval3
elif dataset == 'senseval2':
    files = senseval2
else:
    print >> sys.stderr, "Wrong dataset"
    exit()

for f in files.split():
    for sentence in treebank.parsed_sents(f):
        s = []
        for word, p in sentence.pos():
            if p != '-NONE-':
                s.append(word)
        try:
            print ' '.join(s)
        except TypeError as e:
            print >> sys.stderr, str(e)
            print >> sys.stderr, "This sentence is skipped"

