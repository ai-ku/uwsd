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
from scipy.spatial.distance import pdist, squareform, cosine, euclidean

def get_key_dict(key_f):
    d = dict()
    for line in fopen(key_f):
        word, instance_id, sense = line.split()
        d[instance_id] = sense
    return d

def calc_nearest_neighbors(vectors, dist=euclidean):
    d = {}
    for word, inst_dict in vectors.iteritems():
        indexes = inst_dict.keys()
        M = [inst_dict[instance] for instance in indexes]
        distances = squareform(pdist(M, dist))
        for i, instance in enumerate(indexes):
            ind_dist = zip(indexes, distances[i])
            d[instance] = sorted(ind_dist, key=lambda x: x[1])[1:] # remove itself
    return d

def classify(neighbors, test_inst, exclude_set, key_dict, k):
    d = dd(int)
    closest = [(n,v) for (n, v) in neighbors[test_inst] if n not in exclude_set][:k]
    if len(closest) != 0:
        for (n, v) in closest:
            d[key_dict[n]] += 1
        return max(d, key=lambda n: d[n])
    else:
        return None # we can't decide the label

def get_embedding_vectors(scode_f):

    d = dd(lambda: dict())
    vectors = read_embedding_vectors(scode_f)[0]
    for inst in vectors:
        instance = inst[1:-1]
        word = instance.rsplit('.', 2)[0]
        d[word][instance] = vectors[inst][0]
    return d

def read_test_instances(test_inst_f):
    return set(fopen(test_inst_f).read())

def X_based():
    scode_f = sys.argv[1]
    key_f = sys.argv[2]
    test_inst_f = sys.argv[3] # the file contains the test instances
    max_num_neigh = int(sys.argv[4])
    if sys.argv[5] == 'cosine':
        dist = cosine
    elif sys.argv[5] == 'euclidean':
        dist = euclidean
    else:
        raise ValueError("dist (sys.argv[5]) should be either euclidean or cosine")
    
    key_dict = get_key_dict(key_f)
    embeddings = get_embedding_vectors(scode_f)
    embeddings = get_embedding_vectors('dummy.scode.gz')
    neighbors = calc_nearest_neighbors(embeddings, dist)

    for k in range(1,max_num_neigh):
        for test_instance in fopen(test_inst_f):
            pred_sense = classify(neighbors, test_instance, key_dict, k)
            #TODO: check whether pred_sense is None
            #TODO: write knn.noun.k.ans
            print pred_sense

if __name__ == 'main':
    X_based()
