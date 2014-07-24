#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import nltk
from find_synset_with_oracle import Semantic_Class
from nltk.corpus import wordnet as wn

def calc_sense_prob(x, S):

    """
        This function calculates the probabilities for x (can be a lemma or a key)
        from S (can be a Semantic Class or a Wordnet Synset)


    """

    if isinstance(S, Semantic_Class):
        pass

    elif isinstance(S, nltk.corpus.reader.wordnet.Synset):
        if isinstance(x, nltk.corpus.reader.wordnet.Lemma):
            lemma_count = [lemma.count() for lemma in S.lemmas if lemma == x]
        else:
            lemma_count = [lemma.count() for lemma in S.lemmas if lemma.key == x]

        if len(lemma_count) == 0:
            return 0
        else:
            lemma_count = lemma_count[0]
            total = sum([lemma.count() for lemma in S.lemmas])
            try:
                return lemma_count / float(total)
            except ZeroDivisionError:
                print >> sys.stderr, "Error: There is no count for this synset/SC"
                exit(-1)
    else:
        print >> sys.stderr, "Error: S should be synset or Semantic Class."
        exit(-1)
    

def test():
    car = wn.synsets('car')[0]
    car_lemma = car.lemmas[0]
    car_key = car_lemma.key

    print calc_sense_prob(car_lemma, car)
    print calc_sense_prob(car_key, car)

    assert calc_sense_prob('ahmet', car) == 0, "should be 0!"

    total = 0
    for lemma in car.lemmas:
        c = calc_sense_prob(lemma, car)
        total += c
        print "\t%f" % c

    print "Total:{}".format(total)
    assert total == 1.0, "should be 1.0!"
        
if __name__ == '__main__':
    test()

