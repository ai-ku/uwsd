#!/bin/bash
if [ $# -lt 3 ]; then
  echo $0 train.xml train.key savedir s2 c2
  exit
fi
s2=0
if [ $# -gt 3 ]; then
  s2=$4
fi
c2=0
if [ $# -gt 4 ]; then
  c2=$5
fi
if (set -u; : $WSDHOME) 2> /dev/null
then
  bdir=$WSDHOME
else
  bdir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
fi
libdir=$bdir/lib
CP=$libdir/liblinear-1.33-with-deps.jar:$libdir/jwnl.jar:$libdir/commons-logging.jar:$libdir/jdom.jar:$libdir/trove.jar:$libdir/maxent-2.4.0.jar:$libdir/opennlp-tools-1.3.0.jar:$bdir/ims.jar
export LANG=en_US
java -mx1900m -cp $CP sg.edu.nus.comp.nlp.ims.implement.CTrainModel -prop $libdir/prop.xml -ptm $libdir/tag.bin.gz -tagdict $libdir/tagdict.txt -ssm $libdir/EnglishSD.bin.gz $1 $2 $3 -f sg.edu.nus.comp.nlp.ims.feature.CFeatureExtractorCombination -s2 $s2 -c2 $c2 #-type directory
