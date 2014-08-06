#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

"""
Concatenation of the target word's and the each substitute's embeddings.
Volkan's method
"""

import sys
from nlp_utils import fopen
from fastsub_utils import read_sub_vectors
from embedding_utils import read_embedding_vectors, concat_XYw, get_X, get_Y

embedding_f1 = fopen(sys.argv[1]) # embedding file 1, this provides the X part
embedding_f2 = fopen(sys.argv[2]) # embedding file 2, this provides the Y part
sub_f = fopen(sys.argv[3])   # sub file (we need it for weighting)

subs = read_sub_vectors(sub_f)
embeddingsX = get_X(read_embedding_vectors(embedding_f1))
embeddingsY = get_Y(read_embedding_vectors(embedding_f2))
vectors = concat_XYw(embeddingsX, embeddingsY, subs)
