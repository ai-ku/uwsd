#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module creates a test set according to sys.argv[1] by using Ontonotes.
"""

import sys
from nlp_utils import find_files
import os
import gzip
from nltk.corpus.reader import BracketParseCorpusReader
from collections import defaultdict as dd
from itertools import izip


if len(sys.argv) != 4:
    m = "Usage: {} word_list_file annotated_corpus_path"
    print >> sys.stderr, m.format(sys.argv[0])
    exit(-1)

words = set(open(sys.argv[1]).read().split('\n'))
mapping_file = sys.argv[2] # used for that 
path = sys.argv[3] # annotation path

extension = "*.sense"
fix = {'-LCB-': '{', '-RCB': '}', "n't": 'not', 'ca': 'can', 'wo': 'will', 
      "-LRB-": "(", "-RRB-": ")", "-RSB-": "]", "-LSB-": "[" }


def get_parse_file_dict(annotated_files, words=words):
    d = dd(lambda : dd(list))
    for f in annotated_files:
        parse_file = f.rsplit('.', 1)[0] + ".parse"
        for line in open(f):
            line = line.split()
            w = line[3]
            if w in words:
                sid, tokenid, sense = int(line[1]), int(line[2]), line[-1]
                d[parse_file][sid].append((w, tokenid, sense))
    return d

def write2file(files, lists):
    for f, L in izip(files, lists):
        f.write(" ".join(L))
        f.write('\n')

def create_files(d):
    reader = BracketParseCorpusReader(path, ".*parse")
    print >> sys.stderr, "Reader is created now"
    c = 0
    #filetypes = "pos clean-sent aw.tw sense".split()
    filetypes = "pos clean-sent sense".split()
    files = map(lambda x: gzip.open("ontonotes.%s.gz" % x, 'w'), filetypes)
    for parse_file, sentids in d.viewitems():
        parse_file = '/'.join(parse_file.split('/')[-4:])
        sentences = reader.parsed_sents(parse_file)
        for sentid, triple in sentids.viewitems():
            sentence = sentences[sentid]
            clean_sent_list = []
            clean_pos_list = []
            for word, p in sentence.pos():
                if p != '-NONE-':
                    if word in fix:
                        word = fix[word]
                    clean_sent_list.append(word)
                    clean_pos_list.append(p)
            for w, tid, senseid in triple:
                t = clean_sent_list[tid]
                p = clean_pos_list[tid]
                w = w.replace('-', '.')
                mm = "line-{}\t{}\t{}\t{}\t{}\t{}\t{}".format(c, t, c, tid, p, w, tid)
                ss = "line-{}\t{}\t{}\t{}".format(c, t, w, senseid)
                print mm
                write2file(files, [clean_pos_list, clean_sent_list, [ss]])
                c += 1
    map(lambda f: f.close(), files)

#path = "../data/ontonotes_v5/data/files/data/english/annotations/bc/p2.5_a2e/00/"
annotated_files = find_files(path, extension)
d = get_parse_file_dict(annotated_files, words)
print d.keys()[0]
print d[d.keys()[0]]
exit()
print >> sys.stderr, "Dict created: # of keys: {}".format(len(d))
create_files(d)
