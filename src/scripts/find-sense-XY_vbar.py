#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Convert kmeans output into the Semeval system answer format.
"""

import sys
from collections import defaultdict as dd
import re

regex = re.compile("<((.*\.\w)\.\w+\.\d+)>\s+(\d+)\n")

d = dd(lambda: dd(lambda: dd(int)))

for line in sys.stdin:
    m = regex.match(line)
    inst_id, tw, label = map(m.group, [1,2,3])
    print "{0} {1} {2}-{3}/1.0".format(tw, inst_id, tw, label)
