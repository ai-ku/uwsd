#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import os

c = 1
for line in sys.stdin:
    tw, inst_id, gold_sense = line.split()
    print "{} {} {}-{}".format(tw, inst_id, tw, c)
    c += 1
