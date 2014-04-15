#!/bin/bash
if [ $# -lt 3 ]; then
  echo "$0 modeldir testfile savedir index.sense(option)"
  exit
fi
if (set -u; : $WSDHOME) 2> /dev/null
then
  bdir=$WSDHOME
else
  bdir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
fi
libdir=$bdir/lib
CP=$libdir/liblinear-1.33-with-deps.jar:$libdir/jwnl.jar:$libdir/commons-logging.jar:$libdir/jdom.jar:$libdir/trove.jar:$libdir/maxent-2.4.0.jar:$libdir/opennlp-tools-1.3.0.jar:$bdir/ims.jar
modeldir=$1
testfile=$2
savedir=$3
export LANG=en_US
if [ $# -ge 4 ]; then
  java -mx1900m -cp $CP sg.edu.nus.comp.nlp.ims.implement.CTester -ptm $libdir/tag.bin.gz -tagdict $libdir/tagdict.txt -ssm $libdir/EnglishSD.bin.gz -prop $libdir/prop.xml -r sg.edu.nus.comp.nlp.ims.io.CResultWriter $testfile $modeldir $modeldir $savedir -is $4 -f sg.edu.nus.comp.nlp.ims.feature.CFeatureExtractorCombination
else
  java -mx1900m -cp $CP sg.edu.nus.comp.nlp.ims.implement.CTester -ptm $libdir/tag.bin.gz -tagdict $libdir/tagdict.txt -ssm $libdir/EnglishSD.bin.gz -prop $libdir/prop.xml -r sg.edu.nus.comp.nlp.ims.io.CResultWriter $testfile $modeldir $modeldir $savedir -f sg.edu.nus.comp.nlp.ims.feature.CFeatureExtractorCombination #-type directory
fi
