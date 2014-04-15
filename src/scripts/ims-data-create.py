#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

import sys
from collections import defaultdict as dd
import os


"""struggle.n      struggle.n.on.1 bn/nbc/00/nbc_0039@0039@nbc@bn@en@on-0-6        struggle.n-1    1,3     3.0     0.909090909091  6       And one of the longest running struggles for international justice reached a milestone today of sorts , when a Scottish court , meeting in the Netherlands , finally officially found someone guilty in the 1988 bombing that brought down Pan Am Flight 103 ."""

output_dir = sys.argv[1]

start = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE corpus SYSTEM "lexical-sample.dtd">
<corpus lang="english">
 <lexelt item="{}">\n"""

end = ' </lexelt>\n</corpus>\n'

xml_dict = dd(list)
key_dict = dd(list)

for line in sys.stdin:
    line = line.split('\t')
    lexelt = line[0]
    inst_id = line[1]
    key =  line[3]
    token_id = int(line[7])
    context = line[8].split()
    context[token_id] = "<head>{}</head>".format(context[token_id])
    #print lexelt, '\n', inst_id, '\n', key, '\n', token_id, '\n', context[token_id], '\n'
    # xml entry
    entry = []
    entry.append('\t <instance id="{}">'.format(inst_id))
    entry.append('\t  <answer instance="{}" senseid="{}"/>'.format(inst_id, key))
    entry.append('\t   <context>\n{}\n\t   </context>'.format(' '.join(context)))
    entry.append('\t </instance>\n')
    xml_dict[lexelt].append(entry)
    # key entry
    key_dict[lexelt].append("{} {} {}".format(lexelt, inst_id, key))

# for xml files
for key, entries in xml_dict.viewitems():
    with open(os.path.join(output_dir, key + '.test.xml'), 'w') as f:
        f.write(start.format(key))
        for entry in entries:
            f.write('\n'.join(entry))
        f.write(end)

# For key files
for key, entries in key_dict.viewitems():
    with open(os.path.join(output_dir, key + '.test.key'), 'w') as f:
        for entry in entries:
            f.write("{}\n".format(entry))
