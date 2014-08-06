SHELL := /bin/bash
.SECONDARY:

### 1.1 BIN INSTALLATION
bin:
	cd ../bin; make

### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
export PATH := .:${PATH}:../bin:${SRILM_PATH}:/scratch/1/obaskaya/mapping-impact/run

### Ontonotes Details:
ONTO_ANNOTATION=../data/ontonotes_v5/data/files/data/english/annotations
ONTO_SENSE_INVENTORY=../data/ontonotes_v5/data/files/data/english/metadata/sense-inventories

SRILM_PATH=/opt/srilm/bin/i686-m64
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
SEED=1
SS_JAR=../bin/single-sense-precision.jar
NG_JAR=../bin/weighted-ndcg.jar
PFS_JAR=../bin/pairedFScore.jar
MAP_OPT=2>/dev/null | cut -d '/' -f1 # option arguments for mapping.py

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
export OMP_NUM_THREADS=24

%.sub.gz: %.context.gz
	zcat $< | fastsubs-omp ${FS_OPTIONS} ${LM} | grep -P "^<.*\d>" | gzip > $@
	zcat $< | wc; zcat $@ | wc

%-tw-list.txt: %.all.gz
	zcat $< | cut -f1 | sort | uniq > $@

# IAA based filtering for ontonotes
on-tw-list%.txt: on.all.gz 
	zcat $< | awk -F '\t' '{if ($$7 >= $*) printf("%s\n", $$1)}' | sort | uniq > $@

%.train.context.gz: ukwac.tok.gz ukwac.pos.gz ukwac.lemma.gz %-tw-list.txt
	extract-train-context.py $^ | gzip > $@

%.random.context.gz: %.train.context.gz
	zcat $< | sample-contexts.py 5  | gzip > $@

### POS-based Experiments ###

sampled.tok1.gz sampled.pos1.gz: tok1.gz pos1.gz lemma1.gz
	sample-lines.py ${SEED} 120000 $^

verb.sub.gz noun.sub.gz adj.sub.gz: global.sub.gz
	zcat $< | ./split-vnj.py sampled.lemma1.gz sampled.pos1.gz

verb.pairs.gz: verb.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

noun.pairs.gz: noun.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

adj.pairs.gz: adj.sub.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} | gzip > $@

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

## Key creation. We are using instances whose IAA >= 90
../keys/on.%-0.9.key: on.all.gz
	zcat $< | grep -P "\.$*\t" | awk -F '\t' '{if ($$7 >= 0.9)\
	printf("%s %s %s\n", $$1, $$2, $$4)}' | tee >(wc -l >&2) > $@

## SCODE for POS-Based experiments 
SC_OPTIONS=-s ${SEED} -v 
aiku/%/scode-pos/verb.scode.gz: aiku/%/pairs verb.pairs.gz
	-mkdir aiku/$*/scode-pos/
	zcat $</*.v.pairs.gz verb.pairs.gz | scode ${SC_OPTIONS} | gzip > $@

aiku/%/scode-pos/noun.scode.gz: aiku/%/pairs noun.pairs.gz
	-mkdir aiku/$*/scode-pos/
	zcat $</*.n.pairs.gz noun.pairs.gz | scode ${SC_OPTIONS} | gzip > $@

## ITA=0.9 || S-CODE for POS-Based experiments. 
on.pairs0.9.gz: on.all.gz # list of pairs that have higher IAA than 0.9
	zcat $< | awk -F '\t' '{if ($$7 >= 0.9) printf("%s\t<%s>\n", $$1, $$2)}' |\
	tee >(wc -l >&2) | gzip > $@

on.%.pairs-0.9.gz: on.pairs0.9.gz
	zcat $< | grep -P "\.$*\t" | pair-filtering.py aiku/on/pairs | tee >(gzip > $@) | wc -l

aiku/%/scode-pos-90/verb.scode.gz: on.v.pairs-0.9.gz verb.pairs.gz
	-mkdir aiku/$*/scode-pos-90/
	zcat $^ | scode ${SC_OPTIONS} | gzip > $@

aiku/%/scode-pos-90/noun.scode.gz: on.n.pairs-0.9.gz noun.pairs.gz
	-mkdir aiku/$*/scode-pos-90/
	zcat $^ | scode ${SC_OPTIONS} | gzip > $@

### Clustering substitute word vectors (Y-based approach) ###

KM_OPTIONS=-r 64 -l -w -v -s ${SEED}
aiku/on/km-p/n.Yv.km.%.gz: aiku/on/scode-pos-90/noun.scode.gz
	-mkdir aiku/on/km-p/
	zcat $< | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k $* |\
	gzip > $@

aiku/on/km-p/v.Yv.km.%.gz: aiku/on/scode-pos-90/verb.scode.gz
	-mkdir aiku/on/km-p/
	zcat $< | perl -ne 'print if s/^1://' | wkmeans ${KM_OPTIONS} -k $* |\
	gzip > $@

scores/on.n.Yv.%.score: on.n.pairs-0.9.gz aiku/on/km-p/n.Yv.km.%.gz ../keys/on.n-0.9.key
	zcat $< | find-sense-test.py aiku/on/km-p/n.Yv.km.$*.gz >  ans-Yv-n.k.$*.tmp
	python scorer.py <(python mapping.py ../keys/on.n-0.9.key ans-Yv-n.k.$*.tmp ${MAP_OPT}) \
	../keys/on.n-0.9.key | tee $@
	#tail -1 trash/$@ | tee -a $@
	#java -jar ${SS_JAR} -s ../keys/on.n-0.9.key ans-Yv-n.k.$*.tmp | tail -2 | tee $@
	java -jar ${PFS_JAR} ans-Yv-n.k.$*.tmp ../keys/on.n-0.9.key a | tail -1 | tee -a $@

scores/on.v.Yv.%.score: on.v.pairs-0.9.gz aiku/on/km-p/v.Yv.km.%.gz ../keys/on.v-0.9.key
	zcat $< | find-sense-test.py aiku/on/km-p/v.Yv.km.$*.gz > ans-Yv-v.k.$*.tmp
	python scorer.py <(python mapping.py ../keys/on.v-0.9.key ans-Yv-v.k.$*.tmp ${MAP_OPT}) \
	../keys/on.v-0.9.key | tee $@
	#tail -1 trash/$@ | tee -a $@
	#java -jar ${SS_JAR} -s ../keys/on.v-0.9.key ans-Yv-v.k.$*.tmp | tail -2 | tee $@ 
	java -jar ${PFS_JAR} ans-Yv-v.k.$*.tmp ../keys/on.v-0.9.key a | tail -1 | tee -a $@

### Clustering concatenation of the target word and subs vector: (XY_v vectors) ###

aiku/on/km-p/v.XYv.km.%.gz: aiku/on/scode-pos-90/verb.scode.gz on.v.pairs-0.9.gz
	concat-XY_v.py $^ | wkmeans -r 8 -l -w -v -s ${SEED} -k $* | gzip > $@

aiku/on/km-p/n.XYv.km.%.gz: aiku/on/scode-pos-90/noun.scode.gz on.n.pairs-0.9.gz
	concat-XY_v.py $^ | wkmeans -r 8 -l -w -v -s ${SEED} -k $* | gzip > $@

scores/on.v.XYv.%.score: aiku/on/km-p/v.XYv.km.%.gz ../keys/on.v-0.9.key
	zcat $< | find-sense-XY_v.py > ans-XYv-v.k.$*.tmp
	python scorer.py <(python mapping.py ../keys/on.v-0.9.key ans-XYv-v.k.$*.tmp ${MAP_OPT}) \
	../keys/on.v-0.9.key | tee $@
	#tail -1 trash/$@ | tee -a $@
	#java -jar ${SS_JAR} -s ../keys/on.v-0.9.key ans-XYv-v.k.$*.tmp | tail -2 | tee $@
	java -jar ${PFS_JAR} ans-XYv-v.k.$*.tmp ../keys/on.v-0.9.key a | tail -1 | tee -a $@ 

scores/on.n.XYv.%.score: aiku/on/km-p/n.XYv.km.%.gz ../keys/on.n-0.9.key
	zcat $< | find-sense-XY_v.py > ans-XYv-n.k.$*.tmp
	python scorer.py <(python mapping.py ../keys/on.n-0.9.key ans-XYv-n.k.$*.tmp ${MAP_OPT}) \
	../keys/on.n-0.9.key | tee $@
	#tail -1 trash/$@ | tee -a $@
	#java -jar ${SS_JAR} -s ../keys/on.n-0.9.key ans-XYv-n.k.$*.tmp | tail -2 | tee $@
	java -jar ${PFS_JAR} ans-XYv-n.k.$*.tmp ../keys/on.n-0.9.key a | tail -1 | tee -a $@ 

### Clustering concatenation of the target word and sum of subs vectors: (XYbar vectors)

aiku/on/km-p/v.XYb.km.%.gz: aiku/on/scode-pos-90/verb.scode.gz on.v.pairs-0.9.gz
	concat-XYb.py $^ | wkmeans ${KM_OPTIONS} -k $* | gzip > $@

aiku/on/km-p/n.XYb.km.%.gz: aiku/on/scode-pos-90/noun.scode.gz on.n.pairs-0.9.gz
	concat-XYb.py $^ | wkmeans ${KM_OPTIONS} -k $* | gzip > $@

scores/on.v.XYb.%.score: aiku/on/km-p/v.XYb.km.%.gz ../keys/on.v-0.9.key
	zcat $< | find-sense-XYb.py > ans-XYb-v.k.$*.tmp
	python scorer.py <(python mapping.py ../keys/on.v-0.9.key ans-XYb-v.k.$*.tmp ${MAP_OPT}) \
	../keys/on.v-0.9.key | tee $@
	#tail -1 trash/$@ | tee -a $@
	#java -jar ${SS_JAR} -s ../keys/on.v-0.9.key ans-XYb-v.k.$*.tmp | tail -2 | tee $@
	java -jar ${PFS_JAR} ans-XYb-v.k.$*.tmp ../keys/on.v-0.9.key a | tail -1 | tee -a $@


scores/on.n.XYb.%.score: aiku/on/km-p/n.XYb.km.%.gz ../keys/on.n-0.9.key
	zcat $< | python find-sense-XYb.py > ans-XYb-n.k.$*.tmp
	python scorer.py <(python mapping.py ../keys/on.n-0.9.key ans-XYb-n.k.$*.tmp ${MAP_OPT}) \
	../keys/on.n-0.9.key | tee $@
	#tail -1 trash/$@ | tee -a $@
	#java -jar ${SS_JAR} -s ../keys/on.n-0.9.key ans-XYb-n.k.$*.tmp | tail -2 | tee $@
	java -jar ${PFS_JAR} ans-XYb-n.k.$*.tmp ../keys/on.n-0.9.key a | tail -1 | tee -a $@

on.%.tab: scores
	python score2tab.py $*.Yv.  $< | tee $@
	python score2tab.py $*.XYv. $< | tee -a $@
	python score2tab.py $*.XYb. $< | tee -a $@
	#for p in v n; do \
		#for i in 2 4 8 16 32 64 128 256 512 1024; do \
		 #echo -n $$i"-"$$p"	"; cat $</on.$$p.$*.$$i.score | grep -P "0.\d+"; \
	#done; done | tee $@

### SVM based mapping experiments ###

../keys/gold/%: ../keys/%.keys
	gold-key-splitter.py $< $@

#make n-svm-cv-exp DATASET=aiku/on/ # Check our lexicon mapping idea (Osman and David)
%-svm-cv-exp: ${DATASET}
	cd ${DATASET}; make $*-svm-cv-exp 

### BASELINE
on.mfs.baseline.txt: on.all.gz
	zcat $< | cut -f4 | mfs-baseline.py | tee $@

on.random%.n.baseline.txt: ../keys/on.n-0.9.key
	python random-baseline.py $< $* > $@.tmp
	java -jar ${SS_JAR} -s ../keys/on.n-0.9.key $@.tmp | tail -2 | tee $@
	java -jar ${PFS_JAR} $@.tmp ../keys/on.n-0.9.key   | tail -2 | tee -a $@

on.random%.v.baseline.txt: ../keys/on.v-0.9.key
	random-baseline.py $< $* > $@.tmp
	java -jar ${SS_JAR} -s ../keys/on.v-0.9.key $@.tmp | tail -2 | tee $@ 
	java -jar ${PFS_JAR} $@.tmp ../keys/on.v-0.9.key   | tail -2 | tee -a $@

on.%.1s1i-bs.txt: ../keys/on.%-0.9.key
	cat $< | 1inst1sense-baseline.py > $@

### IMS ###

#make ims/on/test-data
ims/%/testing-data: %.all.gz 
	-mkdir -p $@
	zcat $< | ims-data-create.py $@

ims-wordlist.txt:
	cd ims/ims/models/; ls *.model.gz | sed 's|.model.gz||g' | sort > ../../../$@

ims-tw-test.txt: ims-wordlist.txt on-tw-list.txt
	comm -12 $^ | sort | uniq > $@
	wc $@

ims-tw-test0.9.txt: ims-wordlist.txt on-tw-list0.9.txt
	comm -12 $^ | sort | uniq > $@
	wc $@

ims-run-on: ims-tw-test.txt
	cd ims/ims/; test-ims.sh $<

ims.on.ans: ${ONTO_SENSE_INVENTORY} ~/nltk_data/corpora/wordnet/index.sense
	ims-wn-mapper.py $^ > $@

ims.on.%.ans: ../keys/on.%-0.9.key ims.on.ans
	python ans-filterer.py $^ > $@

scores/ims.on.%.score: ../keys/on.%-0.9.key ims.on.%.ans
	java -jar ${SS_JAR} -s --no-remapping $^ | tail -2 | tee $@ 
	java -jar ${PFS_JAR} ims.on.ans ../keys/on.%-0.9.key | tail -1 | tee -a $@
