#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Split the each target words' answer into a file. Ans file should be in SemEval format
"""

import sys
import os
from collections import defaultdict as dd

system_f = sys.stdin
output_dir = sys.argv[2]
if len(sys.argv) == 3:
    system_f = sys.argv[1] # system key

print >> sys.stderr, len(sys.argv), output_dir

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

tw_f_name = "{}.key"

def get_tw_lines(fn):
    d = dd(list)
    if isinstance(fn, str):
        f = open(fn)
    for line in f:
        L = line.split()
        if len(L) != 0: # some file has empty line at the end of the file
            d[L[0]].append(line)
    return d

def write2file(d):
    for tw, lines in d.viewitems():
        fn = tw_f_name.format(tw)
        with open(os.path.join(output_dir, fn), 'w') as f:
            f.write("".join(lines))

write2file(get_tw_lines(system_f))
