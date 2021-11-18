#!/bin/bash

splitdir=$1
seq_end=$2
zeros=$3
fold=$4

let fold_end=${fold}-1;
let fold_begin=${fold}+1;

fold=`seq -f "%0${zeros}g" ${fold} ${fold}`

# Clean up old junk
mkdir -p ${splitdir}/data${fold}
rm -f ${splitdir}/data${fold}/train.dict

# Create train data
for train_fold in `seq -f "%0${zeros}g" 0 ${fold_end}`; do
  cat ${splitdir}/${train_fold} >> ${splitdir}/data${fold}/train.dict
done
for train_fold in `seq -f "%0${zeros}g" ${fold_begin} ${seq_end}`; do
  cat ${splitdir}/${train_fold} >> ${splitdir}/data${fold}/train.dict
done

# Create gold data
cat ${splitdir}/${fold} \
  | sed "s/*/ /g" \
  > ${splitdir}/data${fold}/test.gold

# Create patterns based on training data
cd ${splitdir}/data${fold}/
../../../tex/make_full_patterns.sh train ../../../tex/sesotho.tr
cd -

# Create test data
cat ${splitdir}/data${fold}/test.gold \
  | sed "s/ //g" \
  > ${splitdir}/data${fold}/test.plain

# Run syllabification system
../tex/syllabifier.py \
  -p ${splitdir}/data${fold}/train.pat \
  -i ${splitdir}/data${fold}/test.plain \
  -o ${splitdir}/data${fold}/test.texsyll

../rule/syllabifier.py \
  -i ${splitdir}/data${fold}/test.plain \
  -o ${splitdir}/data${fold}/test.rulesyll
