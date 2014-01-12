#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
from scipy.linalg import pinv
from scipy.sparse import coo_matrix

wc_data = fopen(sys.argv[1])

def get_data(data_file=wc_data):
    data = []; col = []; row = []
    for line in data_file:
        r, c, d = line.split()
        data.append(float(d))
        row.append(int(r))
        col.append(int(c))
    return row, col, data

row, col, data = get_data()
#M = pinv(coo_matrix((data, (row, col))).todense())
