#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Random baseline creator for Ontonotes dataset
"""

import sys
from nlp_utils import fopen
from random import randint
from collections import defaultdict as dd

test_f = sys.argv[1]
num_of_sense = int(sys.argv[2])

d = dd(list)
for line in fopen(test_f):
    tw, inst_id = line.split()[:2]
    d[tw].append(inst_id)

for tw in sorted(d.keys()):
    for inst_id in d[tw]:
        rsense = randint(1, num_of_sense)
        print "{} {} induced-{}-{}/1.0".format(tw, inst_id, tw, rsense)
