#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

"""
Fetching target words and their ids for all-words task

"""
from uwsd_utils import get_dataset_path
import sys
from bs4 import BeautifulSoup
import re

if len(sys.argv) != 2:
    msg = "Usage: {} dataset_name"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(-1)

dataset = sys.argv[1]
dataset_path = get_dataset_path(dataset)

if dataset == "semeval07":
    line_add = 2
else:
    line_add = 1

soup = BeautifulSoup(open(dataset_path), 'xml')
regex = re.compile('(\w+)\.s(\d+)\.t(\d+)')
if dataset == 'semeval10':
    sentences = soup.find_all('s')
    c = 0
    for sentence in sentences:
        heads = sentence.find_all('head')
        ind = 0
        for i, line in enumerate(sentence.text.split()):
            if ind >= len(heads):
                break
            head = heads[ind]
            if head.text == line:
                matches = regex.search(head['id'])
                sent_id, term_id = map(int, [matches.group(2), matches.group(3)])
                print "{}\t{}\t{}\t{}".format(head['id'], head.text, c, i)
                ind += 1
        c += 1
else:
    heads = soup.find_all('head')
    curr = None
    add = 0
    sent_id = 0
    for head in heads:
        matches = regex.search(head['id'])
        if curr != matches.group(1):
            curr = matches.group(1)
            add += sent_id
            if add != 0:
                add += line_add
        sent_id, term_id = map(int, [matches.group(2), matches.group(3)])
        print "{}\t{}\t{}\t{}".format(head['id'], head.text, sent_id + add, term_id)
