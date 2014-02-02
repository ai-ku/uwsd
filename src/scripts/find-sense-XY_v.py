#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Convert kmeans output into the Semeval system answer format.
"""

import sys
from collections import defaultdict as dd
import re

regex = re.compile("<((.*\.\w)\.\w+\.\d+)>__(\d+)\t(\d+)\n")

d = dd(lambda: dd(lambda: dd(int)))

for line in sys.stdin:
    m = regex.match(line)
    inst_id, tw, count, cls = map(m.group, [1,2,3,4])
    count = int(count)
    d[tw][inst_id][cls] += count

#print everything in semeval format
for tw, instances in d.viewitems():
    for inst_id in instances:
        print "{} {} {}".format(tw, inst_id, " ".join(["{}-{}/{}".format(tw, label, c)
                        for label, c in instances[inst_id].viewitems()]))
