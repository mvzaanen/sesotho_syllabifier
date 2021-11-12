#!/bin/bash

cat dictionary_20201127_syllables.txt \
    | sed "s/.* //" \
    | sed "s/-/*/g" \
    > dictionary_20201127_syllables.dict

./make_full_patterns.sh \
    dictionary_20201127_syllables \
    sesotho.tr
