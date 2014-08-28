#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module makes filtering according to provided gold file and the column no.
Column_no starts with zero

"""

import sys
from nlp_utils import fopen

gold_file = sys.argv[1]
system_file = sys.argv[2]
gold_column_no = int(sys.argv[3]) # gold file column that matches with the system and gold file
target_column_no = int(sys.argv[4]) # gold file column that matches with the system and gold file

instances = set()
for line in fopen(gold_file):
    instance_id = line.split()[gold_column_no]
    instances.add(instance_id)

print >> sys.stderr, len(instances), system_file

for line in fopen(system_file):
    if line.split()[target_column_no] in instances:
        print line,
