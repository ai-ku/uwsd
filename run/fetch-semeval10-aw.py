#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from bs4 import BeautifulSoup

f = '../data/semeval10/aw/test/English/EnglishAW.test.xml'
soup = BeautifulSoup(open(f), 'xml')

sentences = soup.find_all('s')
for sentence in sentences:
    print u' '.join(sentence.text.split()).encode('utf-8').strip()
