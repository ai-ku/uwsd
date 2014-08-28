#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Module creates input for dist to use it. It also creates instances file that contains the mapping for dists
results and the instances.
"""

import sys
from itertools import chain
import gzip


instance_f = gzip.open(sys.argv[1], 'w')


for line in sys.stdin:
    line = line.split()
    m = len(line)
    print >> instance_f, line[0]
    t = zip(range(m-2), map(float, line[2:]))
    values = sorted(t, key=lambda x: x[1], reverse=True)
    print (m-2) * 2, 
    print " ".join(map(str, chain.from_iterable(values)))

instance_f.close()



