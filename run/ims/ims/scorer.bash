#!/bin/bash
if [ $# -lt 1 ]; then
  echo "$0 answerfile keyfile"
  exit
fi
bdir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
libdir=$bdir/lib
testfile=$1
modeldir=$2
savedir=$3
CLASSPATH=$libdir/weka-3.2.3.jar:$libdir/jwnl.jar:$libdir/commons-logging.jar:$libdir/jdom.jar:$libdir/trove.jar:$libdir/maxent-2.4.0.jar:$libdir/opennlp-tools-1.3.0.jar:$libdir/liblinear-1.33-with-deps.jar:$bdir/ims.jar
export LANG=en_US
java -mx1900m -cp $CLASSPATH sg.edu.nus.comp.nlp.ims.util.CScorer $*
