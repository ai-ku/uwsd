#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" This module finds the semantic classes with respect to
    oracle accuracy. Details: The Noisy Channel Paper,
    Algorithm 2.
"""

from nltk.corpus import wordnet as wn
import sys
from nlp_utils import fopen, traverse
from collections import defaultdict as dd
from copy import deepcopy

if len(sys.argv) != 5:
    msg = "Usage: {} key_file number_of_semantic_class"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(1)

class Semantic_Class(object):
    
    def __init__(self, test_synsets=set(), synset=None):
        self.senses = set()
        self.lemma_dict = dd(set)
        self.synsets = dd(set)
        self.test_synsets = test_synsets
        if synset is not None:
            self.add_synset(synset)

    def has_sense(self, sense):
        return sense in self.senses

    def add_synset(self, synset):
        """Add the synset and its all descendants"""
        if self.has_sense(synset):
            msg = "Warning: Semantic Class has already had {} synset".format(synset)
            print >> sys.stderr, msg
        else:
            relation = lambda s: s.hyponyms()
            descendants = synset.tree(relation)
            for descendant in descendants:
                for s in traverse(descendant):
                    for lemma in s.lemmas:
                        if len(self.test_synsets) == 0 or lemma.synset in self.test_synsets:
                            self.senses.add(lemma.key)
                            self.lemma_dict[lemma.name].add(lemma)
                            self.synsets[lemma.name].add(lemma.synset)

    def remove_synset(self, synset):
        """Removes the synset and its all descendants"""
        #TODO: remove all lemmas and its descendant lemmas from senses set
        if self.has_sense(synset):
            relation = lambda s: s.hyponyms()
            descendants = synset.tree(relation)
            for descendant in descendants:
                for s in traverse(descendant):
                    if len(self.test_synsets) == 0 or s in self.test_synsets:
                        for lemma in s.lemmas:
                            #FIXME: descendants may not exist in this semantic class
                            if lemma.name in self.synsets:
                                self.senses.remove(lemma.key)
                                self.lemma_dict[lemma.name].remove(lemma)
                                self.synsets[lemma.name].remove(lemma.synset)
        else:
            msg = "Warning: Semantic Class does not have {} synset".format(synset)
            print >> sys.stderr, msg

    def move_synset_to_another_sm(self, other, synset):
        self.remove_synset(synset)
        other.add_synset(synset)

    def __str__(self):
        return "\n".join([str(s) for s in self.senses])

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

def calc_oracle_accuracy(sc_list):
    return 1

def find_synset_with_best_accuracy(wik, sc_list):
    """According to oracle accuracy, find the best synset to create a new 
       semantic class """
    L = deepcopy(sc_list)
    accuracies = dict()
    for sc in L:
        for synset in sc.synset:
            L = deepcopy(sc_list)
            new_sm = Semantic_Class()
            sc.move_synset_to_another_sm(new_sm, synset)
            L.append(new_sm)
            accuracy = calc_oracle_accuracy(L)
            accuracies[(sc, synset)] = accuracy
    #TODO return synset that maximizes the accuracy

def create_semantic_class(words, pos, test_synsets):
    sm = Semantic_Class(test_synsets)
    for word in words:
        synsets = wn.synsets(word, pos)
        for synset in synsets:
            sm.add_synset(synset)
    return sm

def get_synsets_from_key(keys):
    lemmas = map(wn.lemma_from_key, keys)
    return set([lemma.synset for lemma in lemmas])

def run():
    key_file = sys.argv[1]
    pos_file = sys.argv[2]
    pos = sys.argv[3]
    n = int(sys.argv[4]) # number of semantic class we need to create

    wik = filter_by_pos(read_all_words(key_file), pos, pos_file)
    test_synsets = get_synsets_from_key([t[2] for t in wik if t[2].find('%') != -1])
    sm = create_semantic_class([t[1] for t in wik], pos, test_synsets)
    sc_list = [sm]
    for i in xrange(n):
        synset = find_synset_with_best_accuracy(wik, sc_list)
        new_sm = Semantic_Class(test_synsets, synset)
        sc_list.append(new_sm)

run()
