#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
kNN algorithm using scode vectors
"""

import sys
from nlp_utils import fopen
from collections import defaultdict as dd

scode_f = sys.argv[1]
key_f = sys.argv[2]
test_inst_f = sys.argv[3] # the file contains the test instances
max_num_neigh = int(sys.argv[4])


def get_key_dict():
    """ read key file and get {instance_id : gold_sense} dict"""
    pass

def read_scode_vectors():
    """Read Scode file and get {instance_id : ScodeVector} dict
       Skip the instances in the test file.
    """
    pass

def calc_nearest_neighbors(vectors):
    pass

def get_nearest_neighbors():
    pass

def classify(test_inst):
    # FIXME: some splitting, slicing need to be done
    neighbors = get_nearest_neighbors(test_instance)[k]
    senses = dd(int)
    for neighbor in neighbors:
        gold_sense = key_dict[neighbor]
        senses[gold_sense] += 1

    return max(senses, key = lambda s: senses[s])

vectors = read_scode_vectors()
key_dict = get_key_dict()

nearest_neighbors = {}
calc_nearest_neighbors()

k = 4 # TODO: make an iteration on range(1, max_num_neigh, 2)
for test_instance in fopen(test_inst_f):
    pred_sense = classify(test_instance)
    #TODO: write knn.noun.k.ans


