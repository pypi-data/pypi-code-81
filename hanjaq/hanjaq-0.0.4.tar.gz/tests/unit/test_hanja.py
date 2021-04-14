#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains unit tests related to retrieving information about Hanja characters.

import pytest
import unittest.mock as mock

from hanjaq.exception import NotASingleCharacter
from hanjaq.exception import NotAHanjaCharacter
from hanjaq.hanja import get_hanja_information
from hanjaq.hanja import is_hanja


def test_get_hanja_information_success_known_character():
    """ Tests that we can determine the meaning and hangul representation
        of a Hanja character.
    """
    d = {"漢": (["한"], "<meaning>")}
    with mock.patch("hanjaq.hanja.build_hanja_dict", return_value=d):
        assert get_hanja_information("漢") == (["한"], "<meaning>")


def test_identify_hanja_success_unknown_character():
    """ Tests that empty strings are returned in the case of an uncommon
        Hanja character that is not supported.
    """
    d = {"漢": (["한"], "<meaning>")}
    with mock.patch("hanjaq.hanja.build_hanja_dict", return_value=d):
        assert get_hanja_information("卿") == ([], "")


def test_identify_hanja__exception_not_a_single_character():
    """ Tests that an appropriate exception is raised when input is malformed.
    """
    with pytest.raises(NotASingleCharacter):
        get_hanja_information("漢漢")


def test_identify_hanja__exception_not_a_hanja_character():
    """ Tests that an appropriate exception is raised when input is malformed.
    """
    with pytest.raises(NotAHanjaCharacter):
        get_hanja_information("a")


def test_is_hanja_character__true():
    """ Tests that Hanja characters are correctly identified.
    """
    assert is_hanja("漢")


def test_is_hanja_character__false():
    """ Tests that other characters are correctly identified.
    """
    assert not is_hanja("a")
    assert not is_hanja("한")


def test_is_hanja_character__exception_not_a_single_character():
    """ Tests that an appropriate exception is raised when input is malformed.
    """
    with pytest.raises(NotASingleCharacter):
        is_hanja("aa")
