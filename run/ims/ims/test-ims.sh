#!/bin/bash
test_data_dir=../on/testing-data
if [ $# -lt 1 ]; then
  echo $0 wordlist-file
  exit
fi

for lemma in `cat ../../$1`; do
    model_dir=../on/trained-ims-models
    output_dir=../on/testing-output
    if [ ! -e $output_dir ] ; then
        #mkdir -p $output_dir/{semcor,uniform}
        mkdir -p $output_dir
    fi

    echo $lemma
    ./test_one.bash $model_dir \
        $test_data_dir/$lemma.test.xml $output_dir

    
    # IMS doesn't include the document in its result, so we add it to
    # turn the result into a key
    ims_key=$output_dir/$lemma.ans
    mv $output_dir/$lemma.result $ims_key
    gold_key=$test_data_dir/$lemma.key

    # feel free to score the keys here, or wait until later
    #./scorer.py $ims_key $gold_key
done
