#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for functionality to interact with files.

import djangokeys.utils.strings as m


def test__anonymize_str__0():
    """ An empty string results in an empty string.
    """
    assert m.anonymize_str('') == ''


def test__anonymize_str__1():
    """ A string that consists of a single character is not hidden.
    """
    assert m.anonymize_str('a') == 'a'


def test__anonymize_str__2():
    """ A string that consists of two characters is not hidden.
    """
    assert m.anonymize_str('aa') == 'aa'


def test__anonymize_str__n():
    """ Non-extreme characters of a string are hidden.
    """
    assert m.anonymize_str('abcdefgh') == 'a******h'
