#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from collections import defaultdict as dd

gold_file = open(sys.argv[1])

d = dd(lambda : dd(int))

for line in gold_file:
    line = line.split()
    pw, key = line[0], line[-1]
    d[pw][key] += 1

num_inst = 0
correct = 0
for pw in d:
    key_nums = d[pw].values()
    total = sum(key_nums)
    num_mfs = max(key_nums)
    correct += num_mfs
    num_inst += total

print d[pw]
print "Total number of pseudowords: {}".format(len(d))
print "MFS Score: {}".format(correct / float(num_inst))
print "{} correct of {}".format(correct, num_inst)
print "Avg. correct num of instances {}".format(correct / float(len(d)))


