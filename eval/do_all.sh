#!/bin/bash

# input file
arg=$1
input_file=`basename $arg`
input_dir=`dirname $arg`
# number of parallel processes
par_proc=8
bins=10
zeros=3 # padding zeros

if [ ! -e $input_dir/$input_file ]; then
    echo "$input_dir/$input_file does not exist"
    exit
fi
dos2unix $input_dir/$input_file

input="${input_file%.txt}"
splitdir="${input}_splits"
output="${input}.accuracy.csv"

mkdir -p ${splitdir}

shuf ${input_dir}/${input_file} \
    | sed "s/.* //" \
    | sed "s/-/*/g" \
    > ${splitdir}/${input}.rnd
    #split -d -a ${zeros} -l 1 ${splitdir}/${input}.rnd ${splitdir}/
split -d -a ${zeros} -n r/${bins} ${splitdir}/${input}.rnd ${splitdir}/

let seq_end=${bins}-1;
./parallel -j ${par_proc} \
    "./do_experiment.sh ${splitdir} ${seq_end} ${zeros}" \
    `seq 0 ${seq_end}`
    #    `seq -f "%0${zeros}g" 0 ${seq_end}`

# Clean output file and add header
echo "system,fold,error,total,accuracy" > ${output}
for fold in `seq -f "%0${zeros}g" 0 ${seq_end}`; do
    # Handle texsyll
    let error=`diff ${splitdir}/data${fold}/test.gold ${splitdir}/data${fold}/test.texsyll | grep -c "^<"`
    let total=`cat ${splitdir}/data${fold}/test.texsyll | wc -l`
    echo -n "tex,${fold},${error},${total}," >> ${output}
    echo "(${total} - ${error}) / ${total}" | bc -l >> ${output}

    # Handle rules
    let error=`diff ${splitdir}/data${fold}/test.gold ${splitdir}/data${fold}/test.rulesyll | grep -c "^<"`
    let total=`cat ${splitdir}/data${fold}/test.rulesyll | wc -l`
    echo -n "rule,${fold},${error},${total}," >> ${output}
    echo "(${total} - ${error}) / ${total}" | bc -l >> ${output}
done

# Extract errors
echo > texsyll.errors
echo > rulesyll.errors
for fold in `seq -f "%0${zeros}g" 0 ${seq_end}`; do
    # Handle texsyll
    echo "fold ${fold}" >> texsyll.errors
    diff ${splitdir}/data${fold}/test.gold ${splitdir}/data${fold}/test.texsyll >> texsyll.errors

    # Handle rules
    echo "fold ${fold}" >> rulesyll.errors
    diff ${splitdir}/data${fold}/test.gold ${splitdir}/data${fold}/test.rulesyll >> rulesyll.errors
done
