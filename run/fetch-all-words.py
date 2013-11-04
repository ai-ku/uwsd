#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nltk.corpus.reader import BracketParseCorpusReader
import sys
import gzip
from uwsd_utils import get_dataset_path
import os

dataset=sys.argv[1]

path = os.path.dirname(get_dataset_path(dataset))

sent_error = ["Ruth K. Nelson Cullowhee , N.C .", ]
sent_error = set(sent_error)

if path is None:
    print >> sys.stderr, "Wrong dataset"
    exit(1)

fnames = "clean-sent sent pos".split()
files = map(lambda x: gzip.open("{}.{}.gz".format(dataset, x), 'w'), fnames)

def write2file(lines, files):
    for line, f in zip(lines,files):
        try:
            f.write(" ".join(line))
            f.write('\n')
        except TypeError: # tree parsing error
            print lines

reader = BracketParseCorpusReader(path, '.*mrg')
for fileid in reader.fileids():
    for sentence in reader.parsed_sents(fileid):
        clean_sent_list = []
        sent_list = []
        pos_list = []
        for word, p in sentence.pos():
            if p != '-NONE-':
                clean_sent_list.append(word)
            sent_list.append(word)
            pos_list.append(p)
        lines = [clean_sent_list, sent_list, pos_list]
        write2file(lines, files)

map(lambda f: f.close(), files)
