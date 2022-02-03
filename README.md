# Sesotho syllabifier

Within this project, syllabification systems for Sesotho are developed.  At the moment, two systems are available:

1. Rule-based system: This system can be found in the `rule` directory.
2. TeX-based system: This system can be found in the `tex` directory.

The syllabification systems take as input Sesotho words and provides a syllabified version of the words as output.

Quoting Wikipedia [Wikipedia syllable](https://en.wikipedia.org/wiki/Syllable)
> A syllable is a unit of organization for a sequence of speech sounds.  It is typically made up of a syllable nucleus with optional initial and final margins.  Syllables are often considered the phonological "building blocks" of words.


## Getting started

### Interfaces

The interface of the syllabification systems is essentially the same for both systems with only one difference.  Both systems can be started by running the Python script `syllabifier.py` (in either the `rule` or `tex` directories).  This script reads Sesotho words from an input file and provides the syllabified version of these words in the output file.

The `syllabifier.py` script expects at least two arguments: `-i` or ``--input`` that requires a filename of a text file containing the Sesotho words and `-o` or `--output` that requires a filename in which the syllabified version of the input Sesotho words are stored.

Additional arguments are `-h` or `--help` which provides the usage of the Python scripts, and `-d` or `--debug` which turns on debug information when running the script.

The TeX-based system requires an additional argument `-p` or `--patterns` which requires a patterns file.  This file can be created using TeX's hyphenation system.  The required scripts for these are provided in the package as well, however, the `patgen` system.  The `patgen` system can be found at [CTAN](https://ctan.org/pkg/patgen) and is distributed with programs coming from the TeX project.  The easiest way of creating the patterns file is through the `do_all.sh` bash script.  This script takes one argument, which is a plain text file containing training data.  The content of the training data file is converted to the correct format and is then passed on to the `make_full_patterns.sh` bash script.  This script cidentifies useful patterns and creates `sesotho.tr`, which can be used as the patterns file.


### File formats

The project uses four types of files for input and output.

1. Input file format: The syllabification Python scripts take as input a plain text file (e.g., UTF8) containing one Sesotho word per line.  Note that any whitespace at the right side of the word will be removed.
2. Output file format: The syllabfication Python scripts contain (after running the script) the syllabified version of the words found in the input file.  The syllable boundaries are indicated by spaces (within the word).
3. Pattern file format: The pattern file (automatically generated using the `make_full_patterns.sh` script and stored in `sesotho.tr`) used in the TeX-based system (`tex` directory).  As such, the output is the output that comes from the `patgen` system.
4. Annotated training and testing data: In order to train and test the systems, annotated data is required.  This type of file contains one Sesotho word per line in an plain text file.  Each line contains a word, followed by a space, followed by an annotated version of the word where syllables are indicated by dashes (`-`).


### Required tools

The syllabification scripts are written in Python 3.  For the TeX-based system, bash scripts are used in addition to the Python 3 script.  These scripts have been tested with GNU bash, version 5.0.17(1)-release.  The TeX-based system also relies on the `patgen` tool, which can be found in TeX (or LaTeX) packages.  The systems have been tested with PATGEN 2.4 (TeX Live 2019/Debian).


### Evaluation

The package also contains an evaluation system.  The evaluation system takes annotated data and performs 10-fold cross validation.  The results of the experiments are stored.  This system can be found in the `eval` directory.  This directory contains three bash scripts.  The main script to use is the `do_all.sh` script.  The `do_all.sh` script takes one argument, which is a filename containing annotated data.

The `do_all.sh` script converts the annotated data (which it finds from the argument of the script) splits it into 10 folds.  Note that the number of folds can be adjusted by editing the `do_all.sh` script by modifying the `bin` variable in the `do_all.sh` script.  Next, the script runs `do_experiment.sh` on the different folds.  The `do_experiment.sh` runs experiments for one individual fold both for the rule-based and TeX-based systems.  Finally, the `do_all.sh` script combines the results from both systems and stores the results in a CSV file and additional files indicating the specific errors.

The `do_all.sh` script takes one argument that points to the annotated data.  This file should have a `.txt` file extension.  The evaluation system takes the argument, and splits the dirname from the basename.  It creates a directory containing the 10CV splits which is named `${basename}_splits` (with `${basename}` reprlaced by the actual basename.  The results of the experiments are stored in `${basename}.accuracy.csv`.  Within this file, five columns are found.
1. system: This indicates which system this result belongs to.  Currently, this can be either `tex` or `rule`.
2. fold: This indicates the specific fold.  When running 10CV (which s the default), this runs from 000 to 009.
3. error: This indicates the number of errors made by the system for the specific test fold.
4. total: This denotes the total number of words in the test fold.
5. accuracy: This is the accuracy of the specific system on the specific fold.

The files that have the `.errors` file extension indicate the specific errors made by the system.  It is created using the `diff` script and as such uses that output.


# Contributors

Johannes Sibeko  
`Johannes.Sibeko@mandela.ac.za`  
Nelson Mandela University, University Way, Summerstrand, Gqeberha 6019, South Africa

Menno van Zaanen  
`menno.vanzaanen@nwu.ac.za`  
South African Centre for Digital Language Resources, Internal Box 340, Private bag X6001, Potchefstroom 2520, South Africa
