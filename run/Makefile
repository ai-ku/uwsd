SHELL := /bin/bash
.SECONDARY:

### 1.1 BIN INSTALLATION
bin:
	cd ../bin; make

### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:../bin:${SRILM_PATH}

### Ontonotes Details:
ONTO_ANNOTATION=../data/ontonotes_v5/data/files/data/english/annotations
ONTO_SENSE_INVENTORY=../data/ontonotes_v5/data/files/data/english/metadata/sense-inventories

SRILM_PATH=/opt/srilm/bin/i686-m64
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1
SS_JAR=../bin/single-sense-precision.jar
NG_JAR=../bin/weighted-ndcg.jar

#TEST=$(shell find ../data/pos-filtering/ -name "*.raw.gz" | sort)

### 2.2 SRILM options:
LM_NGRAM=4 # n-gram order
LM_VOCAB=5 # words seen less than this in GETTRAIN will be replaced with <unk>
LM_MTYPE=i686-m64 # architecture for compiling srilm

LM=enw.lm.gz

system_initialization:
	make init-aiku
	make init-ims
	make init-hdp
	make init-ensemble
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/train.lemma.gz ukwac.lemma.gz
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/train.pos.gz ukwac.pos.gz
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/train.tok.gz ukwac.tok.gz
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/tok1.gz 
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/pos1.gz 
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/lemma1.gz 
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/global.sub.gz 
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/sampled.lemma1.gz 
	-ln -s /scratch/1/obaskaya/semeval13-task13/run/sampled.pos1.gz 

init-%:
	-mkdir $*; cd $*; mkdir s07aw s10aw s2aw s3aw on s07wsi s10wsi s2wsi s3wsi;

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

s10aw.clean-sent.gz:
	fetch-semeval10-aw.py | gzip > $@

%.aw.tw.gz:
	fetch-aw-tw.py $* | gzip > $@
	zcat $@ | wc

%.aw.tw.pos.gz: %.aw.tw.gz %.pos.gz
	aw-add-pos.py $^ | gzip > $@

s07aw.key: ../data/semeval07/key/english-all-words.test.key
	cat $< | sed -r 's|<answer head="(\w+)(.*)" senseid="(.*(::)?)"/>|\1 \1\2 \3|g' > $@

s2aw.key: ../data/senseval2/english-all-words/test/key
	cp $< $@

s3aw.key: ../data/senseval3/EnglishAW.test.key
	cp $< $@

%.aw.tw.all.gz: %.pos.gz %.aw.tw.pos.gz
	index-correct.py $^ | gzip > $@

%.context.gz: %.aw.tw.all.gz %.clean-sent.gz
	extract-sem-context.py $^ | gzip > $@

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

### Ontonotes Test set ###

on.all.gz: 
	ontonotes-preprocess.py ${ONTO_ANNOTATION} ${ONTO_SENSE_INVENTORY} | gzip > $@
	zcat $@ | wc

../keys/on.keys.gz: on.all.gz
	zcat $< | cut -f1,2,4 | awk '{printf "%s %s %s\n", $$1, $$2, $$3}' | gzip > $@

../keys/on.%.keys: ../keys/on.keys.gz
	zcat $< | grep -P "\w+\.$* " > $@

on.context.gz: on.all.gz
	zcat $< | cut -f2,8,9 | extract-test-context.py | tee >(gzip > $@) | wc

FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}
export OMP_NUM_THREADS=10

%.sub.gz: %.context.gz
	zcat $< | fastsubs-omp ${FS_OPTIONS} ${LM} | grep -P "^<.*\d>" | gzip > $@
	zwc $<; zwc $@

%-tw-list.txt: %.all.gz
	zcat $< | cut -f1 | sort | uniq > $@

%.train.context.gz: ukwac.tok.gz ukwac.pos.gz ukwac.lemma.gz %-tw-list.txt
	extract-train-context.py $^ | gzip > $@

%.random.context.gz: %.train.context.gz
	zcat $< | sample-contexts.py 5  | gzip > $@

### POS-based Experiments ###

sampled.tok1.gz sampled.pos1.gz: tok1.gz pos1.gz lemma1.gz
	sample-lines.py ${SEED} 120000 $^

verb.sub.gz noun.sub.gz adj.sub.gz: global.sub.gz
	zcat $< | ./split-vnj.py sampled.lemma1.gz sampled.pos1.gz

%.noun.pairs.gz: %.sub.gz
	zcat $< | grep -P "^<\w+\.n" > n.tmp
	perl -le 'print "n.tmp" for 1..100' | xargs cat | wordsub -s ${SEED} | gzip > $@
	rm n.tmp

%.verb.pairs.gz: %.sub.gz
	zcat $< | grep -P "^<\w+\.v" > v.tmp
	perl -le 'print "v.tmp" for 1..100' | xargs cat | wordsub -s ${SEED} | gzip > $@
	rm v.tmp

%.adj.pairs.gz: %.sub.gz
	zcat $< | grep -P "^<\w+\.a" > a.tmp
	perl -le 'print "a.tmp" for 1..100' | xargs cat | wordsub -s ${SEED} | gzip > $@
	rm a.tmp

substitute-sep-%: %.sub.gz
	-rm -rf aiku/$*/sub/ 
	-mkdir aiku/$*/sub/
	zcat $< | separate-sub.py aiku/$*/sub/

aiku/on/pairs/%.pairs.gz: aiku/on/sub/%.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

aiku/%/pairs: aiku/%/sub
	-rm -rf $@; mkdir $@
	for s in `ls $</*sub.gz`; do \
		out= echo -n $$s | sed -e 's|.sub.gz|.pairs.gz|g' -e 's|/sub/|/pairs/|g'; \
		echo "$$out";\
	done | xargs -n1 -P40 make

### POS-BASED EXPERIMENTS

# SCODE for POS-Based experiments
SC_OPTIONS=-s ${SEED} -v 
aiku/%/scode-pos/verb.scode.gz: aiku/%/pairs %.verb.pairs.gz
	-mkdir aiku/$*/scode-pos/
	zcat $</*.v.pairs.gz $*.verb.pairs.gz | scode ${SC_OPTIONS} | gzip > $@

aiku/%/scode-pos/noun.scode.gz: aiku/%/pairs %.noun.pairs.gz
	-mkdir aiku/$*/scode-pos/
	zcat $</*.n.pairs.gz $*.noun.pairs.gz | scode ${SC_OPTIONS} | gzip > $@

### Clustering substitute word vectors (Y-based approach) ###

KM_OPTIONS=-r 8 -l -w -v -s ${SEED}
aiku/on/kmeans-pos/n.Yv.km.%.gz: aiku/on/scode-pos/noun.scode.gz
	-mkdir aiku/on/kmeans-pos/
	zcat $< | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k $* |\
	gzip > $@

aiku/on/kmeans-pos/v.Yv.km.%.gz: aiku/on/scode-pos/verb.scode.gz
	-mkdir aiku/on/kmeans-pos/
	zcat $< | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k $* |\
	gzip > $@

scores/on.n.Yv.%.score: aiku/on/pairs aiku/on/kmeans-pos/n.Yv.km.%.gz ../keys/on.n.keys
	zcat $</*.n.pairs.gz |\
	find-sense-test.py aiku/on/kmeans-pos/n.Yv.km.$*.gz > ans1.k=$*.tmp
	java -jar ${SS_JAR} -s ../keys/on.n.keys ans1.k=$*.tmp | tee $@ | tail -2
	#rm ans1.tmp

scores/on.v.Yv.%.score: aiku/on/pairs aiku/on/kmeans-pos/v.Yv.km.%.gz ../keys/on.n.keys
	zcat $</*.v.pairs.gz |\
	find-sense-test.py aiku/on/kmeans-pos/v.Yv.km.$*.gz > ans2.k=$*.tmp
	java -jar ${SS_JAR} -s ../keys/on.v.keys ans2.k=$*.tmp | tee $@ | tail -2
	#rm ans2.tmp

### Clustering concatenation of the target word and subs vector: (XY_v vectors) ###

aiku/on/kmeans-pos/v.XYv.km.%.gz: aiku/on/scode-pos/verb.scode.gz aiku/on/pairs/
	concat-XY_v.py $< <(zcat aiku/on/pairs/*.v.pairs.gz) |\
	wkmeans ${KM_OPTIONS} -k $* | gzip > $@

aiku/on/kmeans-pos/n.XYv.km.%.gz: aiku/on/scode-pos/noun.scode.gz aiku/on/pairs/
	concat-XY_v.py $< <(zcat aiku/on/pairs/*.n.pairs.gz) |\
	wkmeans ${KM_OPTIONS} -k $* | gzip > $@

scores/on.v.XYv.%.score: aiku/on/kmeans-pos/v.XYv.km.%.gz ../keys/on.v.keys
	zcat $< | find-sense-XY_v.py > ans3.k=$*.tmp
	java -jar ${SS_JAR} -s ../keys/on.v.keys ans3.k=$*.tmp | tee $@ | tail -2
	#rm ans3.tmp

scores/on.n.XYv.%.score: aiku/on/kmeans-pos/n.XYv.km.%.gz ../keys/on.n.keys
	zcat $< | find-sense-XY_v.py  > ans4.k=$*.tmp
	java -jar ${SS_JAR} -s ../keys/on.n.keys ans4.k=$*.tmp | tee $@ | tail -2
	#rm ans4.tmp

### Clustering concatenation of the target word and sum of subs vectors: (XY_vbar vectors)

aiku/on/kmeans-pos/v.XYvbar.km.%.gz: aiku/on/scode-pos/verb.scode.gz aiku/on/pairs/
	concat-XY_vb.py $< <(zcat aiku/on/pairs/*.v.pairs.gz) |\
	wkmeans ${KM_OPTIONS} -k $* | gzip > $@

aiku/on/kmeans-pos/n.XYvbar.km.%.gz: aiku/on/scode-pos/noun.scode.gz aiku/on/pairs/
	concat-XY_vb.py $< <(zcat aiku/on/pairs/*.n.pairs.gz) |\
	wkmeans ${KM_OPTIONS} -k $* | gzip > $@

scores/on.v.XYvbar.%.score: aiku/on/kmeans-pos/v.XYvbar.km.%.gz ../keys/on.v.keys
	zcat $< | find-sense-XY_vbar.py > ans5.k=$*.tmp
	java -jar ${SS_JAR} -s ../keys/on.v.keys ans5.k=$*.tmp | tee $@ | tail -2
	#rm ans3.tmp

scores/on.n.XYvbar.%.score: aiku/on/kmeans-pos/n.XYvbar.km.%.gz ../keys/on.n.keys
	zcat $< | find-sense-XY_vbar.py > ans6.k=$*.tmp
	java -jar ${SS_JAR} -s ../keys/on.n.keys ans6.k=$*.tmp | tee $@ | tail -2

on.%.tab: scores
	for p in v n; do \
		for i in 3 8 16 25 32 64 125 250 500; do \
			echo -n $$i"-"$$p"	"; cat $</on.$$p.$*.$$i.score | tail -2 | head -1 | cut -f4;\
	done; done | tee $@

### BASELINE

on.mfs.baseline.txt: on.all.gz
	zcat $< | cut -f4  | mfs-baseline.py | tee $@
	#java -jar ${SS_JAR} -n ../keys/on.v.keys mfs.v.ans

