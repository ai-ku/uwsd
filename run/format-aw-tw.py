#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

"""
Format the target word file (necessary for pos separation)
"""

import sys

if len(sys.argv) != 2:
    msg = "Usage: {} dataset_name"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(-1)

data = sys.argv[1]

