#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
Automate unscrambling words to cheat at sextuple.
https://apps.apple.com/us/app/sextuple-word-lite/id291026377
August 2019 mlf

TODO: sort in order of first 6 letter word
"""

import sys
import itertools


def unscramble(scrambled_word, target_length, dictionary):
    """
    Return a sorted list of words that are in the dictionary and have
    length == target_length.

    :param  scrambled_word: (str) the word to unscramble.
    :param  target_length: (int) length of words to consider in the dictionary.
        This value is passed to itertools.permutations().
    :param  dictionary: (set) list of english words to each check candidate word against.
        (NOTE: This is an actual dictionary, not the Python data structure.)
    :returns : (list) sorted list of words that meet the length criteria.
    """
    word_list = set()
    for letters in itertools.permutations(scrambled_word, r=target_length):
        # this join is necessary because itertools.permutations returns a tuple
        # like this: ('a', 'b', 'c')
        candidate = ''.join(letters)
        if candidate in dictionary:
            word_list.add(candidate)
    return sorted(word_list)


def test():
    # simple positive test
    assert unscramble('tra', 3, {'art', 'rat', 'tar'}) == ['art', 'rat', 'tar']

    # ignore unrelated words in dictionary
    assert unscramble('tra', 3, {'art', 'arts', 'rat', 'rats', 'star', 'tar', 'tars'}) == ['art', 'rat', 'tar']

    # word ("art") not in dictionary
    assert unscramble('tra', 3, {'rat', 'tar'}) == ['rat', 'tar']

    # negative test - wrong target length, expect empty set
    assert unscramble('tra', 4, {'art', 'rat', 'tar'}) == []
    print('All tests passed')

    # negative test - empty dictionary, expect empty set
    assert unscramble('tra', 4, {}) == []


def main():
    """
    Main function
    - Read dictionary file(s), call unscramble, and print the list of matching words.
    :return: 0 on success or 1 on error
    """
    if len(sys.argv) < 2:
        print('Please provide a six letter word to unscramble.')
        return 1

    scrambled_word = sys.argv[1]
    if len(scrambled_word) != 6:
        print('The scrambled word must be exactly six letters long.')
        return 1

    # primary dictionary
    with open('linuxwords.txt', 'r') as f:
        # this is a set comprehension
        dictionary = {line.rstrip('\n') for line in f}

    # also use supplemental dictionary if exists
    try:
        with open('morewords.txt', 'r') as f:
            # this is a set comprehension union with the primary dictionary
            dictionary |= {line.rstrip('\n') for line in f}
    except FileNotFoundError:
        pass

    # reversed range to print highest value (longest) words first
    for length in [6, 5, 4, 3]:  # reversed(range(3, 7))
        unscrambled_words = unscramble(scrambled_word, length, dictionary)
        if unscrambled_words:
            print("{} letter words".format(length))
            for word in unscrambled_words:
                print(word)
        else:
            print("There are no {} letter words".format(length))

    return 0


if __name__ == '__main__':
    test()
    sys.exit(main())
