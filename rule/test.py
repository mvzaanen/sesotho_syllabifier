#!/usr/bin/env python3
"""test.py

This program tests the syllabification system.
"""

import unittest
import syllabifier

class TestUtils(unittest.TestCase):
    """
    This class tests the utility functions of the syllabification system.
    """

    def test_is_vowel(self):
        """
        Test whether is_vowel works correctly.
        """
        for vowel in "aeiou":
            self.assertTrue(syllabifier.is_vowel(vowel))
            self.assertTrue(syllabifier.is_vowel(vowel.upper()))
        for consonant in "bcdfghjklmnpqrstvwxyz":
            self.assertFalse(syllabifier.is_vowel(consonant))
            self.assertFalse(syllabifier.is_vowel(consonant.upper()))

    def test_is_consonant(self):
        """
        Test whether is_consonant works correctly.
        """
        for consonant in "bcdfghjklmnpqrstvwxyz":
            self.assertTrue(syllabifier.is_consonant(consonant))
            self.assertTrue(syllabifier.is_consonant(consonant.upper()))
        for vowel in "aeiou":
            self.assertFalse(syllabifier.is_consonant(vowel))
            self.assertFalse(syllabifier.is_consonant(vowel.upper()))

    def test_is_single_nasal_or_l(self):
        """
        Test whether is_single_nasal_or_l works correctly.
        """
        for nasal in "nml":
            self.assertTrue(syllabifier.is_single_nasal_or_l(nasal))
            self.assertTrue(syllabifier.is_single_nasal_or_l(nasal.upper()))
        for non_nasal in "abcdefghijkopqrstuvwxyz":
            self.assertFalse(syllabifier.is_single_nasal_or_l(non_nasal))
            self.assertFalse(syllabifier.is_single_nasal_or_l(non_nasal.upper()))

    def test_is_complex_nasal(self):
        """
        Test whether is_complex_nasal works correctly.
        """
        for letter1 in "n":
            for letter2 in "gy":
                self.assertTrue(syllabifier.is_complex_nasal(letter1, letter2))
                self.assertTrue(syllabifier.is_complex_nasal(letter1.upper(), letter2))
                self.assertTrue(syllabifier.is_complex_nasal(letter1, letter2.upper()))
                self.assertTrue(syllabifier.is_complex_nasal(letter1.upper(), letter2.upper()))
            for letter2 in "abcdefhijklmnopqrstuvwxz":
                self.assertFalse(syllabifier.is_complex_nasal(letter1, letter2))
                self.assertFalse(syllabifier.is_complex_nasal(letter1.upper(), letter2))
                self.assertFalse(syllabifier.is_complex_nasal(letter1, letter2.upper()))
                self.assertFalse(syllabifier.is_complex_nasal(letter1.upper(), letter2.upper()))

        for letter1 in "abcdefghijklmopqrstuvwxyz":
            for letter2 in "abcdefghijklmnopqrstuvwxyz":
                self.assertFalse(syllabifier.is_complex_nasal(letter1, letter2))
                self.assertFalse(syllabifier.is_complex_nasal(letter1.upper(), letter2))
                self.assertFalse(syllabifier.is_complex_nasal(letter1, letter2.upper()))
                self.assertFalse(syllabifier.is_complex_nasal(letter1.upper(), letter2.upper()))


class TestRules(unittest.TestCase):
    """
    This class tests the rule functions of the syllabification system.
    """
    def test_Vi_rule(self):
        """
        Test whether the Vi rule works correctly.
        Vi indicates that if we have a vowel at the beginning of the
        word, then it is a syllable.
        """
        # if the index is at the beginning of the word (i.e., index =
        # 1)
        self.assertTrue(syllabifier.Vi_rule("abc", 1))
        self.assertFalse(syllabifier.Vi_rule("bbc", 1))
        # if the index is not at the beginning of the word (i.e., index =
        # 1)
        self.assertFalse(syllabifier.Vi_rule("abc", 2))
        self.assertFalse(syllabifier.Vi_rule("bbc", 2))
        # extreme values of index
        self.assertFalse(syllabifier.Vi_rule("abc", 0))
        self.assertFalse(syllabifier.Vi_rule("abc", -1))
        self.assertFalse(syllabifier.Vi_rule("aaa", 5))

    def test_Vii_rule(self):
        """
        Test whether the Vii rule works correctly.
        Vii indicates that if we have multiple vowels in a row, the
        last one will be a syllable.
        """
        # test regular cases
        self.assertTrue(syllabifier.Vii_rule("aac", 2))
        self.assertTrue(syllabifier.Vii_rule("aaac", 3))
        
        # test beginning and middle vowels
        self.assertFalse(syllabifier.Vii_rule("abc", 1))
        self.assertFalse(syllabifier.Vii_rule("aaa", 1))
        self.assertFalse(syllabifier.Vii_rule("aaa", 2))
        self.assertFalse(syllabifier.Vii_rule("aaac", 2))
        self.assertFalse(syllabifier.Vii_rule("aaaa", 2))
        self.assertFalse(syllabifier.Vii_rule("aaaa", 3))

        # extreme values of index
        self.assertFalse(syllabifier.Vii_rule("aaa", 0))
        self.assertFalse(syllabifier.Vii_rule("aaa", -1))
        self.assertFalse(syllabifier.Vii_rule("aaa", 5))

    def test_V_rule(self):
        """
        Test whether the V rule works correctly.
        The V rule triggers if any of the Vi or Vii rules trigger.
        """
        pass

    def test_C_rule(self):
        """
        Test whether the C rule works correctly.
        C indicates that if we have one of the four nasal consonants
        or the /l/ followed by another consonant (looking to the right
        of the position) then it is a syllable.
        """
        pass

    def test_CV_rule(self):
        """
        Test whether the CV rule works correctly.
        CV indicates that if there is a vowel and one or more
        consonants before it then it is a syllable.
        """
        self.assertTrue(syllabifier.CV_rule("cabc", 2))
        self.assertTrue(syllabifier.CV_rule("ccabc", 3))
        self.assertTrue(syllabifier.CV_rule("ccab", 3))

        self.assertFalse(syllabifier.CV_rule("abc", 1))
        self.assertFalse(syllabifier.CV_rule("caa", 1))
        self.assertFalse(syllabifier.CV_rule("aabc", 2))
        self.assertFalse(syllabifier.CV_rule("cca", 2))
        self.assertFalse(syllabifier.CV_rule("cca", 3))

        # extreme values of index
        self.assertFalse(syllabifier.CV_rule("bac", 0))
        self.assertFalse(syllabifier.CV_rule("bac", -1))
        self.assertFalse(syllabifier.CV_rule("bac", 5))

    def test_syllabify(self):
        """
        Test whether the syllabify function works correctly.
        """
        pass


def main():
    """
    This main function starts the unit test main function.
    """
    unittest.main()


if __name__ == '__main__':
    main()
