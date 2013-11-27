SHELL := /bin/bash
### PATH
export PATH := .:${PATH}:/work/_upos_new/bin:.:${SRILM_PATH}

SRILM_PATH=/opt/srilm/bin/i686-m64
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1

#TEST=$(shell find ../data/pos-filtering/ -name "*.raw.gz" | sort)
#ls *.key | sed 's|.key||g' > ../../../run/existed-twitter-pseudoword-list.txt


### 1.3 INPUT files:
TRAIN=/work/upos/data/wsj.tok.gz 
TESTHEAD=1560570 # The first line of PTB-WSJ in TRAIN (same as first line of TEST)
TESTTAIL=1613710 # The last line of PTB-WSJ in TRAIN (last line of TEST is 1612868)
GETTRAIN=zcat ${TRAIN} | perl -ne 'print if ($$. < ${TESTHEAD} || $$. > ${TESTTAIL})'

### 2.2 SRILM options:
LM_NGRAM=4 # n-gram order
LM_VOCAB=5 # words seen less than this in GETTRAIN will be replaced with <unk>
LM_MTYPE=i686-m64 # architecture for compiling srilm

LM=ukwac.lm.gz

%.vocab.gz: ${TRAIN}
	${GETTRAIN} | ngram-count -write-order 1 -text - -write - | \
	perl -lane 'print $$F[0] if $$F[1] >= ${LM_VOCAB}' | gzip > $@

%.lm.gz: %.vocab.gz ${TRAIN} 
	${GETTRAIN} | ngram-count -order ${LM_NGRAM} -kndiscount \
	-interpolate -unk -vocab $< -text - -lm $@

%.ppl.gz: %.lm.gz
	zcat *.clean-sent.gz | ngram -unk -order ${LM_NGRAM} -ppl - -lm $<

# for senseval2, senseval3, semeval2007
%.aw.fetch:
	fetch-all-words.py $* 

semeval10.clean-sent.gz:
	fetch-semeval10-aw.py | gzip > $@

%.aw.tw.gz:
	fetch-aw-tw.py $* | gzip > $@
	zcat $@ | wc

%.aw.tw.pos.gz: %.aw.tw.gz %.pos.gz
	aw-add-pos.py $^ | gzip > $@

semeval07.key: ../data/semeval07/key/english-all-words.test.key
	cat $< | sed -r 's|<answer head="(\w+)(.*)" senseid="(.*(::)?)"/>|\1 \1\2 \3|g' > $@

senseval2.key: ../data/senseval2/english-all-words/test/key
	cp $< $@

senseval3.key: ../data/senseval3/EnglishAW.test.key
	cp $< $@

%.aw.tw.all.gz: %.pos.gz %.aw.tw.pos.gz
	index-correct.py $^ | gzip > $@

%.context.gz: %.aw.tw.all.gz %.clean-sent.gz
	extract-test-context.py $^ | gzip > $@

FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

%.all.sub.gz: %.context.gz
	zcat $< | fastsubs ${FS_OPTIONS} ${LM} | gzip > $@

%.sub.gz: %.all.sub.gz
	zcat $< | grep -P "^<.*\d>" | gzip > $@
	zcat $@ | wc
	zcat $*.context.gz | wc

# Creates matrix and %.words.gz
%.wc.n.matrix.gz: %.sub.gz %.context.gz
	create-wc-matrix.py $^ n | gzip > $@

# Creates matrix and %.words.gz
%.wc.v.matrix.gz: %.sub.gz %.context.gz
	create-wc-matrix.py $^ v | gzip > $@

.SECONDARY:
