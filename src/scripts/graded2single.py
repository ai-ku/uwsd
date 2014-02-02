#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys


for line in sys.stdin:
    line = line.split()
    stuples = [sense.split('/') for sense in line[2:]]
    stuples = max([(sname, float(d)) for sname, d in stuples], \
                                key= lambda x : x[1])
    line = [line[0], line[1], stuples[0] + '/' + str(stuples[1])]
    print ' '.join(line)
