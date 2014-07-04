#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Concatenation of the target word's and the each substitute's embeddings.
In the thesis, this is named as XY_v.
"""

import sys
from nlp_utils import fopen
from collections import defaultdict as dd

scode_f = fopen(sys.argv[1]) # scode output
pairs_f = fopen(sys.argv[2]) # pairs file (wordsub output)

pairs = dd(lambda: dd(int))
substitutes = set() # all substitutes that any X have

for line in pairs_f:
    X, Y = line.split()
    pairs[X][Y] += 1
    substitutes.add(Y)

print >> sys.stderr, "pairs are read."

sc_vectors = dict()
for i, line in enumerate(scode_f):
    line = line.split()
    w = line[0][2:]
    if line[0].startswith("0:") or w in substitutes:
        sc_vectors[w] = "\t".join(line[2:])

print >> sys.stderr, "scode vectors are read."

for X, d in pairs.iteritems():
    for Y, count in d.iteritems():
        print "{0}__{1}\t{2}\t{3}\t{4}".format(X, count, count, sc_vectors[X], sc_vectors[Y])

print >> sys.stderr, "concetanation is done."
