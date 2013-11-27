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
from multiprocessing import Pool

class Semantic_Class(object):
    
    def __init__(self, test_synsets=set(), synset=None):
        self.senses = set()
        self.lemma_sense = dd(set)
        self.synsets = dd(set)
        self.synset_set = set()
        self.test_synsets = test_synsets
        if synset is not None:
            self.add_synset(synset)

    def has_sense(self, sense):
        return sense in self.senses

    def has_synset(self, synset):
        return synset in self.synset_set

    def add_synset(self, synset):
        """Add the synset and its all descendants"""
        relation = lambda s: s.hyponyms()
        descendants = synset.tree(relation)
        for descendant in descendants:
            for s in traverse(descendant):
                if len(self.test_synsets) == 0 or s in self.test_synsets:
                    self.synset_set.add(s)
                    for lemma in s.lemmas:
                            self.senses.add(lemma.key)
                            lemma_name = lemma.name.lower()
                            self.lemma_sense[lemma_name].add(lemma.key)
                            self.synsets[lemma_name].add(lemma.synset)

    def remove_synset(self, synset):
        """Removes the synset and its all descendants"""
        #TODO: remove all lemmas and its descendant lemmas from senses set
        if self.has_synset(synset):
            relation = lambda s: s.hyponyms()
            descendants = synset.tree(relation)
            for descendant in descendants:
                for s in traverse(descendant):
                    if len(self.test_synsets) == 0 or s in self.test_synsets:
                        #print "\tremoving: {}".format(s)
                        if self.has_synset(s):
                            self.synset_set.remove(s)
                            for lemma in s.lemmas:
                                if lemma.name in self.synsets:
                                    #print lemma, lemma.name, lemma.key, lemma.synset
                                    self.senses.remove(lemma.key)
                                    lemma_name = lemma.name.lower()
                                    self.lemma_sense[lemma_name].remove(lemma.key)
                                    self.synsets[lemma_name].remove(lemma.synset)
        else:
            msg = "Warning: Semantic Class does not have {} synset".format(synset)
            print >> sys.stderr, msg

    def move_synset_to_another_sm(self, other, synset):
        self.remove_synset(synset)
        other.add_synset(synset)

    #def __str__(self):
        #return "\n".join([str(s) for s in self.senses])

def get_synsets_from_key(keys):
    lemmas = map(wn.lemma_from_key, keys)
    return set([lemma.synset for lemma in lemmas])

def read_all_words(key_file):
    with open(key_file) as f:
        wi = []
        for line in f:
            line = line.split()
            inst_id = line[1]
            word = line[2].split('%')[0]
            wi.append((inst_id, word, line[2]))
    return wi

def filter_by_pos(wi, pos, aw_file):
    t = []
    for line in fopen(aw_file):
        line = line.split()
        t.append((line[0], line[4].lower()[0])) #inst_id, pos-tag
    d = dict(t)
    return [(inst_id, word, key) for inst_id, word, key in wi if d[inst_id] == pos]

# (word, instance_id, key triple) list

def get_first_sense(lemma_name, sc):
    lemma_name = lemma_name.lower()
    d = dict([(int(key.split('%')[-1].replace(':', '')), key) \
                                    for key in sc.lemma_sense[lemma_name]])
    return d[min(d)]

def calc_oracle_accuracy(sc_list, gold):
    tf = [] #true false
    for sense in gold:
        if sense != 'U':
            c = None
            for sc in sc_list:
                if sc.has_sense(sense):
                    c = sc
                    break
            assert c is not None, "Error: No semantic class has sense {}".format(sense)
            lemma = sense.split('%')[0]
            first_sense = get_first_sense(lemma, c)
            if first_sense == sense: s = 1
            else: s = 0
            tf.append(s)
    return sum(tf) / float(len(tf))


def _calc(pairs):
    #print >> sys.stderr, "\t\tcalculating started"
    sc, sc_list, synset, gold = pairs
    classes = []
    copy_sc = deepcopy(sc)
    #print len(copy_sc.senses),
    new_sm = Semantic_Class()
    copy_sc.move_synset_to_another_sm(new_sm, synset)
    #print len(copy_sc.senses)
    classes.extend([sclass for sclass in sc_list if sclass is not sc])
    classes.append(copy_sc)
    classes.append(new_sm)
    accuracy = calc_oracle_accuracy(classes, gold)
    #print >> sys.stderr, "\t\tcalculating finished"
    return (synset, (accuracy, classes))

def find_synset_with_best_accuracy(sc_list, test_synsets, gold):
    """According to oracle accuracy, find the best synset to create a new 
       semantic class """
    pool = Pool(processes=20)
    accuracies = dict()
    pairs = []
    for sc in sc_list:
        for synset_sets in sc.synsets.itervalues():
            for synset in synset_sets:
                if synset in test_synsets:
                    pairs.append([sc, sc_list, synset, gold])
    print >> sys.stderr, "\tProcessing starts. # of semantic class {}".format(len(sc_list))
    print >> sys.stderr, "\t{}".format(len(pairs))
    result = pool.map(_calc, pairs[:5])
    accuracies = dict(result)
    key = max(accuracies.iterkeys(), key=lambda x: accuracies[x][0])
    return accuracies[key][1], key, accuracies[key][0]

def create_semantic_class(words, pos, test_synsets):
    sm = Semantic_Class(test_synsets)
    for word in words:
        synsets = wn.synsets(word, pos)
        for synset in synsets:
            sm.add_synset(synset)
    return sm

def run():

    if len(sys.argv) != 5:
        msg = "Usage: {} key_file number_of_semantic_class"
        print >> sys.stderr, msg.format(sys.argv[0])
        exit(1)
    
    key_file = sys.argv[1]
    aw_file = sys.argv[2]
    pos = sys.argv[3]
    n = int(sys.argv[4]) # number of semantic class we need to create

    wik = filter_by_pos(read_all_words(key_file), pos, aw_file)
    test_synsets = get_synsets_from_key([t[2] for t in wik if t[2].find('%') != -1])
    sc = create_semantic_class([t[1] for t in wik], pos, set())
    #sc = create_semantic_class([t[1] for t in wik], pos, test_synsets)
    gold = [t[2] for t in wik]
    sc_list = [sc,]
    scores = []
    for i in xrange(n):
        print >> sys.stderr, "Epoch %d" % (i+1)
        sc_list, sset, score = find_synset_with_best_accuracy (sc_list, test_synsets, gold)
        print >> sys.stderr, "\t{}, {}".format(sset, score)
        scores.append((len(sc_list), score))
    for score in scores:
        print score

def test():
    sm = Semantic_Class()
    air_synsets = wn.synsets('air', 'n')
    for air in air_synsets:
        sm.add_synset(air)
    #sm2 = Semantic_Class()
    #sm.move_synset_to_another_sm(sm2, air)
    #print find_synset_with_best_accuracy([sm])
    print get_first_sense('air', sm)
    print sm.lemma_sense['air']
    print len(sm.synsets)
    #sc_list.append(sm)
    #synset, score = find_synset_with_best_accuracy(sc_list, gold)

def main():
    run()

if __name__ == '__main__':
    main()

