SHELL := /bin/bash

### 1.1 BIN INSTALLATION
bin:
	cd ../bin; make

### PATH
export PATH := .:${PATH}:../bin:${SRILM_PATH}

### Ontonotes Details:
ONTO_ANNOTATION=../data/ontonotes_v5/data/files/data/english/annotations
ONTO_SENSE_INVENTORY=../data/ontonotes_v5/data/files/data/english/metadata/sense-inventories

SRILM_PATH=/opt/srilm/bin/i686-m64
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1

#TEST=$(shell find ../data/pos-filtering/ -name "*.raw.gz" | sort)

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

# Creates matrix and %.words.n.gz
%.wc.n.matrix.gz: %.sub.gz %.context.gz
	create-wc-matrix.py $^ n | gzip > $@

# Creates matrix and %.words.v.gz
%.wc.v.matrix.gz: %.sub.gz %.context.gz
	create-wc-matrix.py $^ v | gzip > $@

ontonotes-stats.txt:
	ontonotes-stats.py ${ONTO_ANNOTATION} ${ONTO_SENSE_INVENTORY} #| tee $@

words-filtered%.txt:
	type-filtering.py ${ONTO_ANNOTATION} ${ONTO_SENSE_INVENTORY} 1 $* > $@
	wc $@

onto-wn%-mapping.txt: words-filtered.txt
	onto-wn-mapper.py ${ONTO_SENSE_INVENTORY} $< $* > $@


### Stemming related ###
mf-stems.%: # most frequent stems for noun verb etc
	cat celex/stemmer.out | awk '{if($$3=="$*" || $$3=="x$*")print $$1,$$2,$$5;}' > tmp
	cat celex-missing-verbs | awk '{print $$1,$$2,1;}' >> tmp
	stem_table.py <(cat tmp | sort) > $@
	rm tmp

coverage.%.N.txt: %.aw.tw.all.gz words-filtered0.txt mf-stems.N
	coverage.py $^

coverage.%.V.txt: %.aw.tw.all.gz words-filtered0.txt mf-stems.V
	coverage.py $^

#ontonotes.aw.tw.gz: words-filtered.txt onto-wn3.0-mapping.txt
	#onto-testset-create.py $^ ${ONTO_ANNOTATION} | gzip > $@

### Ontonotes Test set

ontonotes.all.gz: 
	ontonotes-preprocess.py ${ONTO_ANNOTATION} ${ONTO_SENSE_INVENTORY} | gzip > $@

on.all.context.gz: dummy.all.gz
	zcat dummy.all.gz | cut -f4,8,9 | extract-test-context.py
	#extract-test-context.py $^ 2>onto.context.err | gzip > $@ 

.SECONDARY:
