#!/usr/bin/env python3
"""syllabifier.py

This program takes a file containing a list of words (one per line) as
input.  It writes syllabified versions of the words to output.  The
syllabification boundaries are indicated by -.
"""

import argparse
import logging
import re


def syllabify(word):
    """Apply syllabification to the word and return the syllabified
    word (syllable boundaries indicated by -).
    """
    logging.debug("Syllabifying " + word)
    return word



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
        syl_word = syllabify(word)
        fp_output.write(syl_word)  # Write output to fp_output


if __name__ == '__main__':
    main()
