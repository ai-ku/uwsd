#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import find_files

embeddings_path = sys.argv[1]
output_path = sys.argv[2]
subs_f = sys.argv[3]

X_embeddings_path = "%s/X" % embeddings_path
Y_embeddings_path = "%s/Y" % embeddings_path


#aiku/on/km-p/n.XYv.km.%.gz: aiku/on/scode-pos-90/noun.scode.gz on.n.pairs-0.9.gz
	#concat-XY_v.py $^ | wkmeans -r 8 -l -w -v -s ${SEED} -k $* | gzip > $@

