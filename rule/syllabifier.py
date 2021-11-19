#!/usr/bin/env python3
"""syllabifier.py

This program takes a file containing a list of words (one per line) as
input.  It writes syllabified versions of the words to output.  The
syllabification boundaries are indicated by spaces.
"""

import argparse
import logging
import re

# Functions for checking properties of letters (or combinations of
# letters)

def is_vowel(letter):
    """This function returns true if the letter is a vowel."""
    return letter.lower() in "aeiou"

def is_consonant(letter):
    """This function returns true if the letter is a consonant."""
    return letter.lower() in "bcdfghjklmnpqrstvwxyz"

def is_single_nasal_or_l(letter):
    """This function returns true if the letter is a nasal consonant
    or /l/."""
    return letter.lower() in "nm" or letter.lower() == "l"

def is_complex_nasal(letter1, letter2):
    """This function returns true if the concatenation of letter1 and
    letter2 are the ng, ny, cases"""
    return letter1.lower() == "n" and letter2.lower() in "gy"

# Syllable rules

def Vi_rule(word, index):
    # i if we have a vowel at the beginning of the word, then it is a syllable
    # this only triggers with index == 1.
    return index == 1 and is_vowel(word[index - 1])


def Vii_rule(word, index):
    # ii if we have multiple vowels in a row, the last one will be a syllable
    if index < 1 or index > len(word) - 1:
        return False
    # check if we have at least two vowels before the possible break
    # (index - 2 and index - 1) and check whether the next letter is
    # not a vowel (as then it is not the last vowel in the row.
    # Note that we can always check for the next letter as we test for
    # index > len(word) - 1.
    return index > 1 and is_vowel(word[index - 2]) and is_vowel(word[index - 1]) and not is_vowel(word[index])


def V_rule(word, index):
    # i if we have a vowel at the beginning of the word, then it is a syllable
    # ii if we have multiple vowels in a row, the last one will be a syllable
    # iii similar to V ii (so there is no need to implement this explicitly)
    if index < 1 or index > len(word) - 1:
        return False
    return Vi_rule(word, index) or Vii_rule(word, index)


def C_rule(word, index):
    result = False
    # RULE:
    # M and N
    # When followed by another M or N, then the first M is a syllable [mme = m*me, nna = n*na]
    # When followed by other consonant [mphe = m*phe, ntho = n*tho]
    # When followed by the semi-vowels Y and W, then it is NOT a syllable [nwanya = nwa*nya]
    result = result or (word[index - 1].lower() in "mn" and
            is_consonant(word[index]) and word[index].lower() not in
            "wyg")
    # The letter L
    # When followed by another L, then the first L is a syllable [lla = l*la]
    # When followed by other consonants, then it is NOT a syllable [tlholo = tlho*lo]
    result = result or (word[index - 1].lower() == "l" and
            word[index].lower() == "l")
    # NG and NY
    # When NG is at the end of a word, then it is a syllable [mang*]
    # When followed by the letter W, then it is not a syllable [ngwana = ngwa*na, nwanywetswa = nwa*nywe*tswa]
    result = result or (index > 1 and word[index - 2].lower() == "n" and word[index - 1].lower() == "g" and word[index].lower() == "h")
    # NOTE:
    # NG can be followed by consonant /h/.
    # NY is not followed by any other consonant, the letter W is actually a semi-vowel.
    # The letter NY cannot be at the end of a word.
    return result
 
    # THIS IS THE OLD RULE.  I'm not sure if we need reference to
    # this, but for now, let's keep it here so we can have an easy
    # comparison.
#    # RULE: if we have one of the four nasal consonants or the /l/ followed by another consonant (looking to the right of the position) then it is a syllable
#    if index < 1 or index > len(word) - 1:
#        return False
#    return index > 1 and is_single_nasal_or_l(word[index - 2]) and is_consonant(word[index - 1])


def CV_rule(word, index):
    # RULE: if there is a vowel and one or more consonants before it then it is a syllable
    # index - 1 is the letter before the position where the syllable
    # boundary may be set
    # Check that the index is larger than one, so we also properly
    # check for the consonant
    if index < 1 or index > len(word) - 1:
        return False
    return index > 1 and is_vowel(word[index - 1]) and is_consonant(word[index - 2])


def syllabify(word):
    """Apply syllabification to the word and return the syllabified
    word (syllable boundaries indicated by a space).
    """
    logging.debug("Syllabifying " + word)
    if len(word) <= 1:
        return word
    # For each index in between letters starting from position 1 until the place
    # before the last letter, check if a syllable boundary can be placed there.
    # index indicates the position between letters, so if the word is abcde,
    # index 1 is between a and b.
    syllabified_word = word[0] # Store the first letter as there is never a syllable boundary before the first letter
    for index in range(1, len(word)):
        # This tests all the rules in order.  If one of the rules
        # returns true (i.e., matches), then a syllable boundary is
        # found.
        v_res = V_rule(word, index)
        c_res = C_rule(word, index)
        cv_res = CV_rule(word, index)
        logging.debug("Considering index " + str(index))
        if v_res:
            logging.debug("V rule matched")
        if c_res:
            logging.debug("C rule matched")
        if cv_res:
            logging.debug("CV rule matched")
        if v_res or c_res or cv_res:
            syllabified_word += " "
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
        fp_output.write(syl_word + "\n")  # Write output to fp_output


if __name__ == '__main__':
    main()
