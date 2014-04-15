#!/bin/bash
if [ $# -lt 1 ]; then
  echo $0 input
  exit
fi

#for num_instances in `echo 10 25 50 75 100 150 200 250 500 750 1000 1500 2000 2500 3000 3500 4000 4500 5000`; do
for num_instances in `echo $1`; do
        
    #basedir=fixed-training-data
    basedir=training-data
    dir=has-$num_instances-instances
    output_dir=trained-ims-models/has-$num_instances-instances
    if [ ! -e $output_dir ] ; then
        mkdir $output_dir
    fi

    for prefix in `ls $basedir/$dir | cut -f1,2 -d. | uniq`; do 
        if [ `echo $prefix` != "lexical-sample.dtd" ] 
            then
                ./train_one.bash "$basedir/$dir/$prefix.xml" "training-data/$dir/$prefix.key" "$output_dir"
            fi
    done
    #cat $tmp | xargs --max-args=3 --max-procs=1 ./train_one.bash
done
