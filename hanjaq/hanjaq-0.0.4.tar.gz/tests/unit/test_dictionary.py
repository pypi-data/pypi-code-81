#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains unit tests related to reading information about Hanja from textfile.

import pytest

from hanjaq.dictionary import _extract_information_from_line
from hanjaq.dictionary import DictionaryProblem


def test_extract_information_from_line__success_single_hanja():
    """ Test that fields are correctly parsed and stored.
    """
    d = {}
    _extract_information_from_line(d, "\t".join(["a", "b", "c"]))
    assert "a" in d.keys()
    assert d["a"] == (["b"], "c")


def test_extract_information_from_line__success_multiple_hanja():
    """ Test that fields are correctly parsed and stored when the Hanja field
        contains multiple Hanja characters separated by /.
    """
    d = {}
    _extract_information_from_line(d, "\t".join(["a/b", "c", "d"]))
    assert "a" in d.keys()
    assert d["a"] == (["c"], "d")
    assert "b" in d.keys()
    assert d["b"] == (["c"], "d")


def test_extract_information_from_line__success_multiple_hangul():
    """ Test that fields are correctly parsed and stored when the Hangul field
        contains multiple Hangul representations separated by /.
    """
    d = {}
    _extract_information_from_line(d, "\t".join(["a", "b/c", "d"]))
    assert "a" in d.keys()
    assert d["a"] == (["b", "c"], "d")


def test_extract_information_from_line__failure_too_few_fields():
    """ Test that exception is raised when line contains too few fields.
    """
    d = {}
    with pytest.raises(ValueError):
        _extract_information_from_line(d, "\t".join(["a", "b"]))


def test_extract_information_from_line__failure_too_many_fields():
    """ Test that exception is raised when line contains too many fields.
    """
    d = {}
    with pytest.raises(ValueError):
        _extract_information_from_line(d, "\t".join(["a", "b", "c", "d"]))


def test_extract_information_from_line__failure_malformed_hanja_field():
    """ Test that exception is raised when Hanja field is malformed.
    """
    d = {}
    with pytest.raises(DictionaryProblem):
        _extract_information_from_line(d, "\t".join(["aa", "b", "c"]))


def test_extract_information_from_line__failure_malformed_hangul_field():
    """ Test that exception is raised when Hangul field is malformed.
    """
    d = {}
    with pytest.raises(DictionaryProblem):
        _extract_information_from_line(d, "\t".join(["a", "bc", "d"]))


def test_extract_information_from_line__failure_familiar_hanja():
    """ Test that exception is raised when the same Hanja character is
        added a second time.
    """
    d = {}
    _extract_information_from_line(d, "\t".join(["a", "b", "c"]))
    with pytest.raises(DictionaryProblem):
        _extract_information_from_line(d, "\t".join(["a", "d", "e"]))


def test_extract_information_from_line__failure_familiar_hanja_multiple():
    """ Test that exception is raised when the same Hanja character is
        listed multiple times in the same line.
    """
    d = {}
    with pytest.raises(DictionaryProblem):
        _extract_information_from_line(d, "\t".join(["a/a", "b", "c"]))
