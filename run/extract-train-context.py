#!/usr/bin/env python

import gzip
from itertools import count, izip
import sys
from collections import defaultdict as dd

tw_list = open(sys.argv[4]).read().split()
print >> sys.stderr, "Target word list length: {}".format(len(tw_list))

lemma_pos = dd(lambda: set())
lemma_count = dd(lambda: dict())
lemma_set = set()

INSTANCE_LIMIT = 1000000 # do not go beyond 1M instance

for  tw in tw_list:
    lemma, pos = tw.rsplit('.', 1)
    lemma_pos[lemma].add(pos)
    lemma_count[lemma][pos] = 0
    lemma_set.add(lemma)

f_tok = gzip.open(sys.argv[1])
print >> sys.stderr, "%s loaded" % sys.argv[1]
f_pos = gzip.open(sys.argv[2])
print >> sys.stderr, "%s loaded" % sys.argv[2]
f_lem = gzip.open(sys.argv[3])
print >> sys.stderr, "%s loaded" % sys.argv[3]

for l_tok, l_pos, l_lem, line in izip(f_tok, f_pos, f_lem, count(1)):
    l_tok = l_tok.split()
    l_pos = l_pos.split()
    l_lem = l_lem.split()
    if not (len(l_tok) == len(l_pos) == len(l_lem)):
        sys.stderr.write(str(line) + ': ' + ' '.join(l_tok) + "\n")
        sys.stderr.write(str(line) + ': ' + ' '.join(l_pos) + "\n")
        sys.stderr.write(str(line) + ': ' + ' '.join(l_lem) + "\n")
        continue
    for i in xrange(len(l_lem)):
        if l_lem[i] in lemma_set:
            lemma = l_lem[i]
            pos = l_pos[i][0].lower()
            if pos in lemma_pos[lemma]:
                lemma_count[lemma][pos] += 1
                if lemma_count[lemma][pos] < INSTANCE_LIMIT:
                    print "%s <%s.%s.ukwac.%d> %s" % (' '.join(l_tok[max(0, i - 3):i]),
                                                lemma, pos,
                                                lemma_count[lemma][pos],
                                            ' '.join(l_tok[i + 1:i + 4]))
