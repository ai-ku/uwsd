#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
kNN algorithm using scode vectors
"""

import sys
from nlp_utils import fopen
from collections import defaultdict as dd
from embedding_utils import read_embedding_vectors

def get_key_dict(key_f):
    d = dd(lambda : dict())
    for line in fopen(key_f):
        word, instance_id, sense = line.split()
        d[word][instance_id] = sense
    return d


def calc_nearest_neighbors(vectors, test_instances):
    pass

def get_nearest_neighbors(neighbors, test_instance):
    # example: economy.n.on.1
    word = test_instance.rsplit('.', 2)[0] # economy.n
    return neighbors[word][test_instance]

def classify(neighbors, test_inst, key_dict, k):
    # FIXME: some splitting, slicing need to be done
    k = 5
    neighbors = get_nearest_neighbors(neighbors, test_inst)[1:k+1]
    senses = dd(int)
    for neighbor in neighbors:
        gold_sense = key_dict[neighbor]
        senses[gold_sense] += 1

    return max(senses, key = lambda s: senses[s])

def read_test_instances(test_inst_f):
    return fopen(test_inst_f).read()

def X_based():
    scode_f = sys.argv[1]
    key_f = sys.argv[2]
    test_inst_f = sys.argv[3] # the file contains the test instances
    max_num_neigh = int(sys.argv[4])
    
    vectors = read_embedding_vectors(scode_f)[0]
    key_dict = get_key_dict(key_f)

    neighbors = calc_nearest_neighbors(vectors, test_inst_f)

    k = 4 # TODO: make an iteration on range(1, max_num_neigh, 2)
    for test_instance in fopen(test_inst_f):
        pred_sense = classify(neighbors, test_instance, key_dict, k)
        #TODO: write knn.noun.k.ans

if __name__ == 'main':
    X_based()
