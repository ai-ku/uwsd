#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
from itertools import count
from collections import defaultdict as dd


d = dd(lambda: count(1))

aw_file = sys.argv[1]
sentences = fopen(sys.argv[2]).readlines() # corrected sentences
sentences = [line.split() for line in sentences]

for line in fopen(aw_file):
    line = line.split()
    word, sent_id, tw, offset = line[1], int(line[2]), line[-2], int(line[-1])
    try: 
        p = "%s <%s.%s> %s" % (' '.join(sentences[sent_id][max(0, offset - 3):offset]),
                               tw, d[tw].next(),
                               ' '.join(sentences[sent_id][offset + 1:offset + 4]))
    except IndexError:
        raise IndexError("%s %s" % (line, sentences[sent_id]))
        exit(-1)
    print p

for key, val in d.iteritems():
    print >> sys.stderr, key, '\t', val.next() - 1
