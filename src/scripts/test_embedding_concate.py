#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import os

from embedding_utils import concat_XYw, read_embedding_vectors
from fastsubs_utils import read_sub_vectors


embeddings = read_embedding_vectors('aiku/on/scode-pos-90/noun.scode.gz')
print "reading embedding done"
sub_vectors = read_sub_vectors('dummy.sub.gz')
print "reading subs done"
e1 = embeddings[0] # X
e2 = embeddings[1] # Y

vectors = concat_XYw(e1, e2, sub_vectors)
print vectors[0], vectors[0].shape
