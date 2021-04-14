#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This module is used to read information about Hanja characters from a file.

import os

from hanjaq.exception import DictionaryProblem


def build_hanja_dict():
    """ Returns dictionary that maps hanja characters to their information.

    :return: dictionary containing information about Hanja characters
    :rtype: dict
    """
    if not hasattr(build_hanja_dict, "_hanja_dict"):
        build_hanja_dict._hanja_dict = _build_hanja_dict()  # cached!
    return build_hanja_dict._hanja_dict


def _build_hanja_dict():
    """ Internal function used to construct dictionary that maps Hanja
        characters to their information.

    :return: dictionary containing information about Hanja characters
    :rtype: dict
    """
    hanja_dict = dict()
    for line in _read_file(_get_hanja_txt_filepath()).splitlines():
        if line.strip() == "" or line.startswith("#"):
            continue
        _extract_information_from_line(hanja_dict, line)
    return hanja_dict


def _read_file(filepath):
    """ Returns all content of a textfile as a single string.

    :param str filepath: filepath of file to read contents from

    :return: contents of file with given filepath
    :rtype: str
    """
    with open(filepath, "r") as f:
        s = f.read()
    return s


def _get_hanja_txt_filepath():
    """ Returns filepath of location where hanja.txt is expected to be found.

    :return: filepath of hanja.txt file
    :rtype: str
    """
    this_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(this_dir, "hanja.txt")


def _extract_information_from_line(hanja_dict, line):
    """ Extracts information about Hanja character from line, and stores
        information about Hanja character in a dictionary.

    :param dict hanja_dict: used to store information about Hanja
    :param str line: line containing information about Hanja character
    """
    (hanja_field, hangul_field, meaning_field) = line.split("\t")

    hangul_representations = []
    for hangul_ch in hangul_field.split("/"):
        if len(hangul_ch) != 1:
            msg = "Hangul field isn't properly formatted; line: {}"
            raise DictionaryProblem(msg.format(line))
        hangul_representations.append(hangul_ch)

    for hanja_ch in hanja_field.split("/"):
        if not len(hanja_ch) == 1:
            msg = "Hanja field isn't properly formatted; line: {}"
            raise DictionaryProblem(msg.format(line))
        if hanja_ch in hanja_dict.keys():
            msg = "Tried to add the same hanja character '{}' twice."
            raise DictionaryProblem(msg.format(hanja_ch))
        hanja_dict[hanja_ch] = (hangul_representations, meaning_field)
