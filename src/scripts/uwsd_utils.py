#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

s10aw = "../data/semeval10/aw/test/English/EnglishAW.test.xml"
s10wsi = "../data/semeval10/wsi"
s07aw = "../data/semeval07/all-words/english-all-words.test.xml"
s3aw = "../data/senseval3/english-all-words.xml"
s2aw = "../data/senseval2/english-all-words/test/eng-all-words.test.xml"

def get_dataset_path(dataset):
    path = None
    if dataset == 's07aw':
        path = s07aw
    elif dataset == 's3aw':
        path = s3aw
    elif dataset == 's2aw':
        path = s2aw
    elif dataset == 's10aw':
        path = s10aw
    return path


def main():
    pass

if __name__ == '__main__':
    main()

