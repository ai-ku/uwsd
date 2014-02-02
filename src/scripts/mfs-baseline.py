#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Calculate the mfs score for a given dataset. Input should be the gold standard such as:

car.n-1
go.v-3

"""

import sys
from collections import defaultdict as dd
from nlp_utils import fopen

d = dd(lambda : dd(int))

lines = dd(list)
for line in sys.stdin if len(sys.argv) == 1 else fopen(sys.argv[1]):
    L = line.split()
    tw, gold_sense = L[0], L[-1]
    d[tw][gold_sense] += 1
    lines[tw].append(line)

num_inst = 0
correct = 0
for pw in d:
    key = max(d[pw], key=lambda x: d[pw][x])
    for line in lines[pw]:
        line = line.split()
        print "{} {}".format(' '.join(line[:2]), key)
    key_nums = d[pw].values()
    total = sum(key_nums)
    num_mfs = max(key_nums)
    correct += num_mfs
    num_inst += total

print >> sys.stderr, "Total number of pseudowords: {}".format(len(d))
print >> sys.stderr, "MFS Score: {}".format(correct / float(num_inst))
print >> sys.stderr, "{} correct of {}".format(correct, num_inst)
print >> sys.stderr, "Avg. correct num of instances {}".format(correct / float(len(d)))


