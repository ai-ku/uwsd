#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
kNN implementation

input (sys.stdin): dist file (dists)
k = # of neighbors that need to be considered
"""

import sys
from nlp_utils import fopen
from itertools import izip_longest


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def predict(inst, neighbors, weighting=True):
    senses = dict()
    for neighbor, dist in neighbors:
        key = keys[neighbor]
        val = senses.get(key, 0)
        senses[key] = val + float(dist)
    return min(senses, key=lambda x: senses[x])

k = int(sys.argv[1])
gold_f = fopen(sys.argv[2])

keys = dict() # building the instance_id -> sense dictionary
for line in gold_f:
    word, instance_id, sense = line.split()
    instance_id = "<%s>" % instance_id
    keys[instance_id] = sense

d = dict()
preds = []
for line in sys.stdin:
    line = line.split()
    inst = line[0]
    neighbors = zip(line[1:k*2+1:2], line[2:k*2+1:2])
    pred_sense = predict(inst, neighbors)
    actual_sense = keys[inst]
    preds.append(pred_sense == actual_sense)
    #print inst, keys[inst], pred_sense
    #print preds
    #exit()

print "Accuracy\t%.5f\tk\t%d" % (sum(preds) / float(len(preds)), k)



