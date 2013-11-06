#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip
import sys

tw_lines = gzip.open(sys.argv[1]).readlines()
pos_lines = gzip.open(sys.argv[2]).readlines()

for line in tw_lines:
    line = line.split()
    sent_id, t_id = map(int, line[2:])
    p = pos_lines[sent_id].split()[t_id]
    line.append(p)
    tw = line[1] 
    line.append(tw + "." + p[0].lower())
    print "\t".join(line)
