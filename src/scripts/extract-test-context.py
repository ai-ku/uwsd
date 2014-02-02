#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys

for line in sys.stdin:
    try: 
        instance, tok_id, sentence = line.split('\t')
    except ValueError:
        print >> sys.stderr, "Error:", line
        raise ValueError
    sentence = sentence.split()
    tok_id = int(tok_id)
    print "{} <{}> {}".format(' '.join(sentence[max(0, tok_id - 3):tok_id]),
                             instance,
                            ' '.join(sentence[tok_id + 1:tok_id + 4]))
