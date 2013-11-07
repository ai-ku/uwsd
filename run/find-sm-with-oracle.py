#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" This module finds the semantic classes with respect to
    oracle accuracy. Details: The Noisy Channel Paper,
    Algorithm 2.
"""

from nltk.corpus import wordnet as wn
import sys
from nlp_utils import fopen

if len(sys.argv) != 5:
    msg = "Usage: {} key_file number_of_semantic_class"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(1)

class Semantic_Class(object):
    
    def __init__(self):
        senses = set()
        lemma_dict = dict()

    def has_sense(self, sense):
        return sense in self.senses

    def add_synset(self, synset):
        """Add the synset and its all descendants"""
        #TODO: add all lemmas and its descendant lemmas from senses set
        pass

    def remove_synset(self):
        """Removes the synset and its all descendants"""
        #TODO: remove all lemmas and its descendant lemmas from senses set
        pass

def read_all_words(key_file):
    with open(key_file) as f:
        wi = []
        for line in f:
            line = line.split()
            inst_id = line[1]
            word = line[2].split('%')[0]
            wi.append((inst_id, word, line[2]))
    return wi

def filter_by_pos(wi, pos, pos_file):
    t = []
    for line in fopen(pos_file):
        line = line.split()
        t.append((line[0], line[4].lower()[0])) #inst_id, pos-tag
    d = dict(t)
    return [(inst_id, word, key) for inst_id, word, key in wi if d[inst_id] == pos]

# (word, instance_id, key triple) list

def find_synset_with_best_accurracy(wik, sc_list):
    """According to oracle accuracy, find the best synset to create a new 
       semantic class """
    pass

def create_semantic_class():
    pass


def run():
    key_file = sys.argv[1]
    pos_file = sys.argv[2]
    pos = sys.argv[3]
    n = int(sys.argv[4]) # number of semantic class we need to create
    wik = filter_by_pos(read_all_words(key_file), pos, pos_file)
    create_semantic_class(wik)
    for i in xrange(n):
        find_synset_with_best_accuracy(wik, )
