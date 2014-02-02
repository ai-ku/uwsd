#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Input should follow the Semeval format.
This module makes a sense normalization (all sense gradings are adding up to 1) 
for each instance.
"""

import sys
import numpy as np

for line in sys.stdin:
    line = line.split()
    vals = np.array([sense.split('/')[-1] for sense in line[2:]], dtype='float64')
    vals /= vals.sum()
    senses = [sense.split('/')[0] for sense in line[2:]]
    print "{} {}".format(line[0], line[1]),
    for s, v in zip(senses,vals):
        print "{}/{}".format(s, v),
    print


