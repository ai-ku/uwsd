#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

import sys
from nlp_utils import find_files
import re


#on.n.XYv.128.score

#regex = re.compile('F.*Score.*(0\.\d+)')

pattern = sys.argv[1] # embedding type
directory = sys.argv[2]

regex = re.compile('.*F.*Score.*(0\.\d+).*')
fn_regex = re.compile('scores/on\.(\w)\.(\w+)\.(\d+)\.score')


print directory, pattern

def file_sort(fn):
    return int(fn.split('.')[3])

files = find_files(directory, '*%s*.score' % pattern)
for f in sorted(files, key=file_sort):
    results = []
    for line in open(f):
        match = regex.match(line)
        if match:
            results.append(match.group(1))
    fn_match = fn_regex.match(f)
    print "%s-%s\t" % (fn_match.group(3), fn_match.group(1)),
    print '\t'.join(results)
