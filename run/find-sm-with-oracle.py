#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" This module finds the semantic classes with respect to
    oracle accuracy. Details: The Noisy Channel Paper,
    Algorithm 2.
"""

import nltk.corpora import wordnet as wn
import sys

if len(sys.argv) != 3:
    msg = "Usage: {} key_file number_of_semantic_class"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(1)

key_file = sys.argv[1]
n = int(sys.argv[2]) # number of semantic class we need to create
