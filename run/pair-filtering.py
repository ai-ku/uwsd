#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module is for filtering issues for scode input. on.all.gz file contains 
all instaances in Ontonotes dataset. However, we'd like to use some subset of
it. For instance, we may use only the subset of instances where all instances
have at least 0.9 ITA agreement. Another subset may consist of only Wordnet
3.0 instances. For such circumstances, this module can be used.

INPUT:
- sys.stdin: the list that indicates which instances will be used as scode input.
- pairs directory

"""

import sys
from collections import defaultdict as dd
from nlp_utils import fopen
import os

pairs_d = sys.argv[1]

pairs = dd(set)
for line in sys.stdin:
    tw, inst = line.split()
    #print pair_f, "\t\t", inst
    pairs[tw].add(inst)

sys.stderr.write("pairs dict is loaded.\n")

for tw, S in pairs.viewitems():
    pair_f = "{}.pairs.gz".format(os.path.join(pairs_d, tw))
    for line in fopen(pair_f):
        inst = line.split()[0]
        if inst in S:
            print line,
