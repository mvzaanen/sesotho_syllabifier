#!/usr/bin/env python3
"""convert.py
This program takes a list of syllabified words and converts them into
a format suitable for training in a machine learner.
"""

import argparse
import logging
import re


def convert(syl_word):
    """Convert the syllabified word (syl_word) into a format that can
    be used as input for a machine learner.
    """
    logging.debug("Convert data")
    return syl_word


def main():
    """Commandline arguments are parsed and handled.  Next, the input
    is read from the input filename.  The words found in the input
    file are converted into a format suitable as input for a machine
    learner.  This is then writen to the output file.
    """

    parser = argparse.ArgumentParser(description = "This program converts a list of syllabified words into a format that can be used as input for a machine learner.")
    parser.add_argument("-i", "--input",
        help = "name of input file",
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
        ml_format = convert(word)
        fp_output.write(ml_format)  # Write output to fp_output

if __name__ == '__main__':
    main()
