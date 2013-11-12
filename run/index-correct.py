#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys
from collections import defaultdict as dd
from nlp_utils import fopen

pos_file = sys.argv[1]
aw_file = sys.argv[2]

TAG = "-NONE-"
aw_lines = fopen(aw_file).readlines()

indices = dd(list)
for line in aw_lines:
    line = line.split()
    line_ind = int(line[2])
    term_ind = int(line[3])
    indices[line_ind].append(term_ind)

whole_ind = []
for i, line in enumerate(fopen(pos_file)):
    line = line.split()
    remove = []
    for j, t in enumerate(line):
        if t == TAG:
            remove.append(j)
    m = len(indices[i])
    remove_part = [0] * m
    for j, ind in enumerate(indices[i]):
        rr = 0
        for tag_ind in remove:
            if tag_ind < ind:
                rr += 1
        remove_part[j] = rr
    result = []
    for ind, rem in zip(indices[i], remove_part):
        #print ind, rem
        result.append(ind - rem)
    whole_ind.extend(result)
    #print ' '.join([str(k) for k in result])

for line, new_index in zip(aw_lines, whole_ind):
     line = line.split()
     line.append(str(new_index))
     print "\t".join(line)
