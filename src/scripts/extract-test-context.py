#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys

for line in sys.stdin:
    instance, tok_id, sentence = line.split('\t')
    sentence = sentence.split()
    tok_id = int(tok_id)
    print "{} <{}> {}".format(' '.join(sentence[max(0, tok_id - 3):tok_id]),
                             instance,
                            ' '.join(sentence[tok_id + 1:tok_id + 4]))
