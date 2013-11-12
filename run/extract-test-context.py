#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen

aw_file = sys.argv[1]
sentences = fopen(sys.argv[2]).readlines() # corrected sentences
sentences = [line.split() for line in sentences]

for line in fopen(aw_file):
    line = line.split()
    i_id, tw, sent_id, pos, offset = line[0], line[1], int(line[2]), line[4], int(line[6])
    try: 
        p = "%s <%s.%s.%s> %s" % (' '.join(sentences[sent_id][max(0, offset - 3):offset]),
                                    tw, pos.lower()[0], i_id,
                                    ' '.join(sentences[sent_id][offset + 1:offset + 4]))
    except IndexError:
        print >> sys.stderr, "Error:", line, sentences[sent_id]
        exit()
    print p




