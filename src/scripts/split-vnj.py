#!/usr/bin/env python

from itertools import izip
import gzip
import sys
from collections import defaultdict as dd

LIMIT = 10000 # do not go beyond this number of instance for one type
lemma = []
pos = []

for l, p in izip(gzip.open(sys.argv[1]), gzip.open(sys.argv[2])):
    l = l.split()
    p = p.split()
    assert(len(l) == len(p))
    for l, p in izip(l, p):
        lemma.append(l)
        if p.startswith('NP'): # NP,NPS: proper noun, pn plural, respectively
            pos.append('x') 
        else:
            pos.append(p[0].lower())

write_to = [gzip.open("verb.sub.gz", 'w'),
            gzip.open("noun.sub.gz", 'w'),
            gzip.open("adj.sub.gz", 'w')]


d = dd(int)

for line, l, p in izip(sys.stdin, lemma, pos):
    line = line.split("\t")
    tw = l + '.' + p
    line[0] = tw
    if d[tw] < LIMIT:
        d[tw] += 1
        if p == 'v':
            write_to[0].write("\t".join(line))
        elif p == 'n':
            write_to[1].write("\t".join(line))
        elif p == 'j':
            write_to[2].write("\t".join(line))
