#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains functionality related to dealing with strings.


def anonymize_str(s):
    """ Anonymize a string but leave its first and last characters visible.

    :param str s: a string

    :return: string with all non-extreme characters replaced by *
    :rtype: str
    """
    if len(s) < 3:
        return s
    return s[0] + ("*" * (len(s) - 2)) + s[-1]
