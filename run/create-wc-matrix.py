#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nlp_utils import fopen
import gzip
import sys
from itertools import izip, count
import re
from math import e
from collections import defaultdict as dd

#According -6.92737293   response -7.39505959    according -7.39907217
#Ill Homeless '' <referred.v.d00.s00.t09> to research by

def prob_conv(s):
    return pow(e, float(s))

def index_mapping(subs, contexts, pos):
    regex = re.compile("<.*\.{}\..*\d+>".format(pos))
    c = count(0)
    words = dd(lambda : c.next())
    all_context = dict()
    for sub_line, context_line in izip(subs, contexts):
        sub_line = sub_line.split()
        tw = sub_line[0]

        # pos does not match, skip it
        if regex.match(tw) is None:
            continue

        words_probs = [[sub_line[i], prob_conv(sub_line[i+1])] \
                                for i in xrange(1, len(sub_line)-1, 2)]
        context = context_line.replace(tw, "_XX_")
        if context not in all_context:
            for t in words_probs: #word, probability
                t[0] = words[t[0]]
            all_context[context]= words_probs

    return all_context, words

def format_mapping(all_context):

    data = []; col = []; row = []
    for i, val in enumerate(all_context.itervalues()):
        for v in val:
            r, dat = v
            data.append(dat)
            row.append(r)
            col.append(i)

    return row, col, data

def main():

    if len(sys.argv) != 4:
        msg = "Usage: {} sub_file context_file pos_tag"
        sys.stderr.write(msg.format(sys.argv[0]))
        exit(1)

    subs = fopen(sys.argv[1])
    contexts = fopen(sys.argv[2])
    pos = sys.argv[3]
    
    all_context, words = index_mapping(subs, contexts, pos)
    
    with gzip.open(sys.argv[1].split('.')[0] + ".words." + pos + ".gz", 'w') as f:
        for key, val in words.iteritems():
            f.write("{}\t{}\n".format(val, key))

    row, col, data = format_mapping(all_context)
    for r, c, d in izip(row, col, data):
        print "{} {} {}".format(r,c,d)

if __name__ == '__main__':
    main()

