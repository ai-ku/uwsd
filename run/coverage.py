#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Coverage tests.
-How many words in Ontonotes are also in the test data (SensEval, SemEval)
"""

import sys
import os
from nlp_utils import fopen
from collections import defaultdict as dd

test_file = fopen(sys.argv[1])
ontonotes_file = fopen(sys.argv[2]) # words that filtered from ontonotes
stem_file = fopen(sys.argv[3]) # it comes from celex
POS = sys.argv[3][-1].lower() # noun or verb or adj


d = {}
for line in stem_file:
    word, stem_class = line.split()
    d[word] = stem_class

""" STEM FILE has some missing stems. I add them manually below """

missing_stems = {'homeless': 'homeless',
                 'born' : 'born',
                 'brokering' : 'broker',
                 'disassemble' : 'disassemble',
                 'deprived' : 'deprive',
                 'rendezvoused': 'rendezvous',
                 # senseval2
                 'proteins' : 'protein', #verb
                 'sum' : 'sum', #verb
                 'dna': 'dna',
                 'latent': 'latent',
                 'something': 'something',
                 'ringing': 'ringing',
                 'tracking': 'tracking',
                 }
d.update(missing_stems)

test_words = set()
missing = set()
for line in test_file:
    word, pos = line.split()[-2].lower().rsplit('.', 1) # There are some tw such as Mr..n
    if pos == POS:
        stem = d.setdefault(word, None)
        if stem is None:
            missing.add(word + '.' + POS)
        #print word, stem
        else:
            test_words.add(stem + '.' + POS)

#print temp
m = len(test_words)
n = len(missing)
print >> sys.stderr, "# of missing stems: {} of {}".format(n, m+n)
if n != 0:
    print >> sys.stderr, missing
on_words = set([line.strip().replace('-', '.') for line in ontonotes_file])

diff = test_words.difference(on_words)
print >> sys.stderr, "# of missing words in Ontonotes: {} of {}".format(len(diff), m)

