#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests related to retrieving information about Hanja characters.

from hanjaq import is_hanja


def test_is_hanja_character__true():
    """ Tests that Hanja characters are correctly identified.
    """
    assert is_hanja("漢")


def test_is_hanja_character__false():
    """ Tests that other characters are correctly identified.
    """
    assert not is_hanja("a")
    assert not is_hanja("한")
