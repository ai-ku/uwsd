#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module provides some functionality related to S-CODE vectors
such as reading, vector concetanation and so on.
"""

from nlp_utils import fopen
from collections import defaultdict as dd
#from collections import Counter
import numpy as np
import sys
import gzip

def read_embedding_vectors(embedding_f, wordset=None):
    """ word_set is a set that indicates the tokens to fetch
        from embedding file.
    """
    is_scode_f = False
    if 'scode' in embedding_f:
        is_scode_f = True

    assert isinstance(wordset, set) or wordset == None, "wordset should be a set"

    d = dd(lambda: dict())
    for line in fopen(embedding_f):
        line = line.split()
        if is_scode_f:
            typ = int(line[0][0])
            w = line[0][2:]
            start = 2
            count = int(line[1])
        else:
            typ = 0
            w = line[0]
            start = 1
            count = 1
        if wordset is None or w in wordset :
            d[typ][w] = (np.array(line[start:], dtype='float64'), count)
    return d

def concat_XY(embedding_d, subs):
    d = dd(lambda : dict())
    for X, s in subs.viewitems():
        Xs = Counter(s)
        for Y, count in Xs.viewitems():
            d[X][Y] = (np.concatenate([embedding_d[0][X][0], embedding_d[1][Y][0]]), count)
    return d

def concat_XYbar(embedding_d, subs, dim=25):
    d = dict()
    for X, s in subs.viewitems():
        Y_bar = np.zeros(dim)
        Xs = Counter(s)
        for Y, count in Xs.viewitems():
            Y_bar += embedding_d[1][Y][0] * count
        Y_bar /= (Y_bar.dot(Y_bar) ** 0.5)
        d[X] = (np.concatenate(embedding_d[0][X][0], Y_bar), 1)
    return d

def write_vec(embedding_d, fn=None):
    f = sys.stdout
    if fn is not None:
        f = gzip.open(fn, 'w')
    for word, (vec, count) in embedding_d.viewitems():
        f.write("{}\t{}\t{}".format(word, count, "\t".join(map(str, vec))))

    if fn is not None:
        f.close()
