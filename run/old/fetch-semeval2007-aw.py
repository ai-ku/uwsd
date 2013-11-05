#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from bs4 import BeautifulSoup

f = "../data/semeval07/all-words/english-all-words.test.xml"
soup = BeautifulSoup(open(f), 'xml')

texts = soup.find_all('text')
sentences = []
for t in texts:
    sentence = []
    for token in t.text.split():
        if token == '.':
            sentence.append('.')
            sentences.append(sentence)
            sentence = []
        else:
            if token.startswith("*"):
                continue
            sentence.append(token)

for s in sentences:
    print u' '.join(s).encode('utf-8').strip()
