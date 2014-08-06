#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from nlp_utils import fopen

gold_file = sys.argv[1]
system_file = sys.argv[2]

instances = set()
for line in fopen(gold_file):
    instance_id = line.split()[1]
    instances.add(instance_id)

for line in fopen(system_file):
    if line.split()[1] in instances:
        print line,
