#!/usr/bin/env python3
"""syllabifier.py

This program takes a file containing a list of words (one per line) as
input.  It writes syllabified versions of the words to output.  The
syllabification boundaries are indicated by -.
"""

import argparse
import logging
import re

# Functions for checking properties of letters (or combinations of
# letters)

def is_vowel(letter):
    """This function returns true if the letter is a vowel."""
    return letter in "aeiou"

def is_consonant(letter):
    """This function returns true if the letter is a consonant."""
    return letter in "bcdfghjklmnpqrstvwxz"

def is_nasal_or_l(letter1, letter2):
    """This function returns true if the letter2 is a nasal consonant
    or /l/. Letter1 is checked in the ng, ny, cases"""
    if letter2 in "nm": # check single nasals
        return True
    elif letter2 in "l": # check l
        return True
    elif letter2 in "gy" and letter1 == "n": # check complex nasals
        return True
    return False


# Syllable rules

def Vi_rule(word, index):
    # i if we have a vowel at the beginning of the word, then it is a syllable
    return False


def Vii_rule(word, index):
    # ii if we have multiple vowels in a row, the last one will be a syllable
    return False


def V_rule(word, index):
    # i if we have a vowel at the beginning of the word, then it is a syllable
    # ii if we have multiple vowels in a row, the last one will be a syllable
    # iii similar to V ii (so there is no need to implement this explicitly)
    return Vi_rule(word, index) or Vii_rule(word, index)


def C_rule(word, index):
    # RULE: if we have one of the four nasal consonants or the /l/ followed by another consonant (looking to the right of the position) then it is a syllable
    return False


def CV_rule(word, index):
    # RULE: if there is a vowel and one or more consonants before it then it is a syllable
    # index - 1 is the letter before the position where the syllable
    # boundary may be set
    # Check that the index is larger than one, so we also properly
    # check for the consonant
    return index > 1 and is_vowel(word[index - 1]) and is_consonant(word[index - 2])


def syllabify(word):
    """Apply syllabification to the word and return the syllabified
    word (syllable boundaries indicated by -).
    """
    logging.debug("Syllabifying " + word)
    # For each index in between letters starting from position 1 until the place
    # before the last letter, check if a syllable boundary can be placed there.
    # index indicates the position between letters, so if the word is abcde,
    # index 1 is between a and b.
    syllabified_word = word[0] # Store the first letter as there is never a syllable boundary before the first letter
    for index in range(1, len(word) - 1):
        # This tests all the rules in order.  If one of the rules
        # returns true (i.e., matches), then a syllable boundary is
        # found.
        if V_rule(word, index) or C_rule(word, index) or CV_rule(word, index):
            syllabified_word += "-"
        syllabified_word += word[index]
    return syllabified_word



def main():
    """Commandline arguments are parsed and handled.  Next, the input
    is read from the input filename one word at a time.  The word is
    the syllabified and written to output.
    """

    parser = argparse.ArgumentParser(description="This program reads in a list of words, one per line and adds syllabification boundaries, which is then written to the output file.")
    parser.add_argument("-i", "--input",
        help = "name of text file containing input words",
        action = "store",
        metavar = "FILE")
    parser.add_argument("-o", "--output",
        help = "name of output file",
        action = "store",
        metavar = "FILE")
    parser.add_argument("-d", "--debug",
        help = "provide debugging information",
        action = "store_const",
        dest = "loglevel",
        const = logging.DEBUG,
        default = logging.WARNING,
)
    args = parser.parse_args()

    logging.basicConfig(level = args.loglevel)

    if args.input == None:
        parser.error("An input filename is required.")
    fp_input = open(args.input, "r")

    if args.output == None:
        parser.error("An output filename is required.")
    fp_output = open(args.output, "w")


    for word in fp_input:  # Simply read a line from fp_input
        syl_word = syllabify(word.rstrip()) # Syllabify and remove newline
        fp_output.write(syl_word)  # Write output to fp_output


if __name__ == '__main__':
    main()
