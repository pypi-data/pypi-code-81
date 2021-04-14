#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file contains functionality to get information about Hanja character.

from hanjaq.dictionary import build_hanja_dict
from hanjaq.exception import NotAHanjaCharacter
from hanjaq.exception import NotASingleCharacter

import re


def is_hanja(ch):
    """ Checks if a given character is a Chinese character.

    :param str ch: a character as a string of length 1

    :rtype: bool
    :return: True if it's a Chinese character, False otherwise.

    :raise NotASingleCharacter: argument was not a single character
    """
    if not isinstance(ch, str) or len(ch) != 1:
        msg = "Expected a single character as a string of length 1: {}"
        raise NotASingleCharacter(msg.format(ch))
    return re.search("[\u4e00-\u9FFF]", ch)


def get_hanja_information(ch):
    """ Returns Hangul representation and meaning of a known Hanja character.

    If the Hanja character is not recognized, this function returns a tuple
    with an empty list for Hangul representations, and an empty string as
    its meaning. If it is not a Hanja character, an exception is raised.

    :param str ch: a hanja character as a string of length 1

    :rtype: ([str], str)
    :return: Hangul representation and meaning of Hanja character

    :raise NotASingleCharacter: argument was not a single character
    :raise NotAHanjaCharacter: argument was not a Hanja character
    """
    if not is_hanja(ch):
        msg = "Expected a Hanja character: {}"
        raise NotAHanjaCharacter(msg.format(ch))
    return build_hanja_dict().get(ch, ([], ""))
