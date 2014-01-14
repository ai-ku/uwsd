#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Filter the inventory words that two constraints:
 - ITA degree
 - Sense Inventory (take words that have only wn 3.0 senses)
"""

import sys
import os
from nlp_utils import find_files
from bs4 import BeautifulSoup

#annotations_path = "../data/ontonotes_v5/data/files/data/english/annotations"
#inventory = "../data/ontonotes_v5/data/files/data/english/metadata/sense-inventories"

if len(sys.argv) != 5:
    msg = "Usage: {} annotation_path sense_inventory_path is_only_wn threshold"
    print >> sys.stderr, msg.format(sys.argv[0])

annotations_path = sys.argv[1]
inventory = sys.argv[2]
if sys.argv[3] == '0':
    is_only_wn = False
else:
    is_only_wn = True
threshold = float(sys.argv[4]) / 100

print >> sys.stderr, is_only_wn, threshold

def get_filtered_set(is_only_wn, ita_threshold):
    inventory_files = find_files(inventory, "*.xml")
    for num_processed, f in enumerate(inventory_files):
        fn = os.path.basename(f).replace('.xml', '')
        if num_processed % 1000 == 0:
            print >> sys.stderr, "{} files processed".format(num_processed)
        soup = BeautifulSoup(open(f), 'xml')
        if ita_threshold != 0:
            ita = soup.findAll('ita') # inter-annotator agreement
            if len(ita) != 0:
                ita_score = float(ita[0]['ann_1_2_agreement'])
                if ita_score > ita_threshold:
                    if is_only_wn:
                        versions = [wn['version'] == '3.0' for wn in soup.findAll('wn')[:-1]]
                        if all(versions):
                            print fn
                    else:
                        print fn#, "\t", ita_score
        else:
            if is_only_wn:
                versions = [wn['version'] == '3.0' for wn in soup.findAll('wn')[:-1]]
                if all(versions):
                    print fn
            else:
                print fn
    print >> sys.stderr, "{} files processed in total".format(num_processed+1)

get_filtered_set(is_only_wn, threshold)
