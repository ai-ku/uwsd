#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from nlp_utils import calc_perp, fopen
from collections import defaultdict as dd

key_f = fopen(sys.argv[1])


d = dd(list)
for line in key_f:
    tw, inst_id, tag = line.split()
    d[tw].append(tag)

for tw, labels in d.viewitems():
    print "{}\t{}\t{}".format(tw, len(labels), calc_perp(labels))
