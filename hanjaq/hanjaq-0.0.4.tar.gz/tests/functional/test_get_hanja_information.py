#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests related to retrieving information about Hanja characters.

from hanjaq import get_hanja_information


def test_identify_hanja_success_known_character():
    """ Tests that we can determine the meaning and hangul representation
        of a known Hanja character.
    """
    hangul_representations = ["경"]
    meaning = "noble, high officer: term of respect"
    assert get_hanja_information("卿") == (hangul_representations, meaning)


def test_identify_hanja_success_multiple_hangul_representations():
    """ Tests that correct information is retrieved for Hanja character with
        multiple Hangul representations.
    """
    hangul_representations = ["녀", "여"]
    meaning = "woman, girl"
    assert get_hanja_information("女") == (hangul_representations, meaning)


def test_identify_hanja_success_unknown_character():
    """ Tests that empty strings are returned in the case of an uncommon
        Hanja character that is not known.
    """
    assert get_hanja_information("零") == ([], "")
