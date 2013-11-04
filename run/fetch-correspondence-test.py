#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import gzip

dataset = sys.argv[1]

lines = gzip.open("{}.aw.tw.gz".format(dataset)).readlines()
sentences = gzip.open("{}.sent.gz".format(dataset)).readlines()

num_true = 0
for i, line in enumerate(lines):
    line = line.split()
    tw = line[-3]
    sent_id, term_id = map(int, line[-2:])
    try:
        pred = sentences[sent_id].split()[term_id] 
    except:
        print line
        print "exiting"
        exit(-1)
    if pred != tw:
        print sent_id, term_id, tw, pred
    else:
        num_true += 1

print "Number of target word: {} | True correspondence: {}".format(num_true, i+1)
