#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

semeval10 = "../data/semeval10/aw/test/English/EnglishAW.test.xml"
semeval07 = "../data/semeval07/all-words/english-all-words.test.xml"
senseval3 = "../data/senseval3/english-all-words.xml"
senseval2 = "../data/senseval2/english-all-words/test/eng-all-words.test.xml"

def get_dataset_path(dataset):
    path = None
    if dataset == 'semeval07':
        path = semeval07
    elif dataset == 'senseval3':
        path = senseval3
    elif dataset == 'senseval2':
        path = senseval2
    elif dataset == 'semeval10':
        path = semeval10
    return path


def main():
    pass

if __name__ == '__main__':
    main()

