#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import sys
from collections import defaultdict as dd
import numpy as np
import random
from sklearn.preprocessing import normalize

random.seed(42)

def chunks(l, n):
    """ Yield successive n-sized chunks from l. """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def load_key(fname):

    print >> sys.stderr, "loading %s" % fname
    d = dd(lambda: dd(lambda: dd(lambda : 0.)))

    lines = open(fname).readlines()
    #c = 0
    for line in lines:
        line = line.split()
        key, inst = line[:2]
        senses = line[2:]
        senses = [sense.split('/') for sense in senses]
        if len(senses) == 1:
            #c += 1
            d[key][inst][senses[0][0]] = 1.
        else:
            uni = []
            for sense in senses:
                if len(sense) == 1:
                    uni.append(sense)
                else:
                    d[key][inst][sense[0]] = float(sense[1])
            if len(uni) > 0:
                assert len(uni) != len(senses), "Some sense weighted, some not: %s" % inst
                val = 1. / len(uni)
                for sense in senses:
                    d[key][inst][sense[0]] = val
    return d

def remap(gold_instances, test_instances, training_instances):

    # removing instances that excluded from gold data (e.g. SemEval 2013)
    difference = set(test_instances.keys()).difference(set(gold_instances))
    map(test_instances.pop, difference)

    test_ids = []
    gold_ids = []

    for instance_id in training_instances:
        gs_perception = gold_instances[instance_id]
        ts_perception = test_instances[instance_id]
        if gs_perception is not None and ts_perception is not None:
            test_ids.extend(ts_perception.keys())
            gold_ids.extend(gs_perception.keys())


    gold_ids = set(gold_ids)
    test_ids = set(test_ids)

    m = len(test_ids)
    n = len(gold_ids)

    # for matrix indexing. each different sense gets the index
    if m != 0 and n != 0:
        test_sense_ids = dict(zip(test_ids, range(m)))
        gold_sense_ids = dict(zip(gold_ids, range(n)))

        #print "test senses - ids", test_sense_ids
        #print "gold senses - ids:", gold_sense_ids
        #print

        mapping_matrix = np.zeros([m, n])
    
        for instance_id in training_instances:
            gs_perception = gold_instances[instance_id]
            ts_perception = test_instances[instance_id]
            
            for key, val in ts_perception.iteritems():
                ts_ind = test_sense_ids[key]
                #print ts_ind, key, val, "\t",
                for gold_key, gold_val in gs_perception.iteritems():
                    gs_ind = gold_sense_ids[gold_key]
                    #print gs_ind, gold_key, gold_val
                    score = gold_val * val
                    mapping_matrix[ts_ind, gs_ind] += score
        #print mapping_matrix

        # Normalize the matrix
        mapping_matrix = normalize(mapping_matrix, norm='l1', axis=1)

        #print "After normalization\n", mapping_matrix

        #print "all instances:", test_instances.keys()
        #print "training instances:", training_instances
        test_inst_ids = set(test_instances.keys()).difference(training_instances)
        #print "test instance ids:", test_inst_ids

        remapped = dict()
        for test_inst_id in test_inst_ids:
            test_vector = np.zeros(mapping_matrix.shape[0])
            ts_perception = test_instances[test_inst_id]
            for key, col in test_sense_ids.iteritems():
                if key in ts_perception:
                    test_vector[col] = ts_perception[key]

            result = np.dot(test_vector, mapping_matrix)
            mapped = [(sense, result[ind]) for sense, ind in gold_sense_ids.iteritems() 
                                             if result[ind] != 0]
            if len(mapped) > 0:
                remapped[test_inst_id] = dict(mapped)
            else:
                print >> sys.stderr, "problem for %s" % test_inst_id
            
        return remapped

def print_as_ans_key(lemma, d, one_sense=True):

    def instance_compare(tt):
        return int(tt[0].split('.')[-1])

    for inst_id, sense_dict in sorted(d.iteritems(), key=instance_compare):
        print "{0} {1}".format(lemma, inst_id),
        # sort so that first sense has the maximum degree
        sorted_senses = sorted(sense_dict.iteritems(), key=lambda x: x[1], reverse=True)
        if one_sense:
            sorted_senses = sorted_senses[0:1]
        print " ".join(["{0}/{1}".format(*s) for s in sorted_senses])

def run_eval(lemma, goldkey, testkey, test_sets, all_instances):
    
    all_instances = set(all_instances)
    all_chunks = {}
    for test_instances in test_sets:
        training_instances = all_instances.difference(test_instances)
        remapped_testkey = remap(goldkey, testkey, training_instances)
        if len(training_instances) != 0:
            all_chunks.update(remapped_testkey)
    print_as_ans_key(lemma, all_chunks)
        


goldkey = load_key(sys.argv[1])
testkey = load_key(sys.argv[2])

#NUMBER_OF_CHUNKS = 5
for lemma, inst_dict in sorted(goldkey.iteritems()):
    all_instances = inst_dict.keys()
    random.shuffle(all_instances)
    NUMBER_OF_CHUNKS = len(all_instances) # leave-one-out-cross-validation
    test_sets = list(chunks(all_instances, len(all_instances) / NUMBER_OF_CHUNKS))
    # if division not exact, add all instances in last chunk to previous so that
    # we have NUMBER_OF_CHUNKS chunks.
    if len(test_sets) == NUMBER_OF_CHUNKS+1:
        test_sets[NUMBER_OF_CHUNKS-1].extend(test_sets[NUMBER_OF_CHUNKS])
        test_sets.pop()
    test_sets = [set(t) for t in test_sets]
    if len(testkey[lemma]) != 0:
        run_eval(lemma, goldkey[lemma], testkey[lemma], test_sets, all_instances)
