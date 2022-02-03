#!/bin/bash

arg=$1
basefile=${arg%.txt}

cat ${basefile}.txt \
    | sed "s/.* //" \
    | sed "s/-/*/g" \
    > ${basefile}.dict

./make_full_patterns.sh \
    ${basefile} \
    sesotho.tr
