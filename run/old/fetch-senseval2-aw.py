#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nltk.corpus import treebank

files = "wsj_0089.mrg  wsj_0465.mrg  wsj_1286.mrg".split()

for f in files:
    for sentence in treebank.parsed_sents(f):
        s = []
        for word, p in sentence.pos():
            if p != '-NONE-':
                s.append(word)
        print ' '.join(s)


# old version
#f = '../data/senseval2/english-all-words/test/eng-all-words.test.xml'
#soup = BeautifulSoup(open(f), 'xml')

#texts = soup.find_all('text')
#sentences = []
#quot_set = set(['"', ])
#quot = False
#sentence = []
#for t in texts:
    #tokens = t.text.split()
    #for token in tokens:
        #if token in quot_set:
            #quot = not quot
        #if token == '.' and not quot:
            #sentence.append('.')
            #sentences.append(sentence)
            #sentence = []
        #else:
            #sentence.append(token)

#for s in sentences:
    #print u' '.join(s).encode('utf-8').strip()

# a = sinica_treebank.read_sexpr_block(open('aa'))[0]
# Tree(a).leaves() 
