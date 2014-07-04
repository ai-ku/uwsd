#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

import sys

file1 = set(open(sys.argv[1]).readlines())
file2 = set(open(sys.argv[2]).readlines())
print "File1 has %d different entity" % len(file1.difference(file2))
print "File2 has %d different entity" % len(file2.difference(file1))





