#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple utility functions used by Open Tree python code.

These function are used by packages that descend from peyotl, but
do not depend on any part of peyotl.
"""
from __future__ import absolute_import, print_function, division

__version__ = '0.0.4'  # sync with setup.py

import time
import os


def any_early_exit(iterable, predicate):
    """Tests each element in iterable by calling predicate(element).

    Returns True on first True, or False.
    """
    for i in iterable:
        if predicate(i):
            return True
    return False


def pretty_timestamp(t=None, style=0):
    """NOT Recommended. Simple time formatter. legacy artifact!

    Used in peyotl test reporting.
    `t` defaults to current time.
    If `style` is 0, strftime uses Y-m-d format
    If `style` is not 0 and  not a string YmdHMS is the format.
    Otherwise it is passed to strftime.
    """
    if t is None:
        t = time.localtime()
    if isinstance(style, int) and style == 0:
        style = "%Y-%m-%d"
    elif not isinstance(style, str):
        style = "%Y%m%d%H%M%S"
    if isinstance(t, time.struct_time):
        return time.strftime(style, t)
    return t.strftime(style)


def doi2url(v):
    """Canonicalizes a DOI.

    Takes a string form of a DOI (raw, http..., or doi:) and returns
    a string in the URL form.
    """
    if v.startswith('http'):
        return v
    if v.startswith('doi:'):
        if v.startswith('doi: '):
            v = v[5:]  # trim 'doi: '
        else:
            v = v[4:]  # trim 'doi:'
    if v.startswith('10.'):  # it's a DOI!
        return 'http://dx.doi.org/' + v
    # convert anything else to URL and hope for the best
    return 'http://' + v


def get_unique_filepath(stem):
    """Returns a unique stem# string. NOT thread-safe!

    Return stems or stem# where # is the smallest
    positive integer for which the path does not exist.
    useful for temp dirs where the client code wants an
    obvious ordering.
    """
    fp = stem
    if os.path.exists(stem):
        n = 1
        fp = stem + str(n)
        while os.path.exists(fp):
            n += 1
            fp = stem + str(n)
    return fp


def propinquity_fn_to_study_tree(inp_fn, strip_extension=True):
    """For internal use only. Parses a filename to study+tree.

    This should only be called by propinquity - other code should be treating these
    filenames (and the keys that are based on them) as opaque strings.

    Takes a filename (or key if strip_extension is False), returns (study_id, tree_id)

    propinquity provides a map to look up the study ID and tree ID (and git SHA)
    from these strings.
    """
    if strip_extension:
        study_tree = '.'.join(inp_fn.split('.')[:-1])  # strip extension
    else:
        study_tree = inp_fn
    x = study_tree.split('@')
    if len(x) != 2:
        msg = 'Currently we are expecting studyID@treeID.<file extension> format. ' \
              'Expected exactly 1 @ in the filename. Got "{}"'
        msg = msg.format(study_tree)
        raise ValueError(msg)
    # snakemake-based propinquity prefixes ID with "tree_"
    if x[0].startswith('tree_'):
        x[0] = x[0][5:]
    return x


# Make the following names visible to client code using "from peyutil import ..."
from .input_output import (download,
                           expand_path,
                           expand_to_abspath,
                           open_for_group_write,
                           parse_study_tree_list,
                           pretty_dict_str,
                           read_as_json,
                           read_filepath,
                           write_to_filepath,
                           write_as_json,
                           write_pretty_dict_str, )

from .str_util import (flush_utf_8_writer,
                       get_utf_8_string_io_writer,
                       increment_slug, is_int_type, is_str_type,
                       primitive_string_types,
                       reverse_dict,
                       slugify, StringIO,
                       underscored2camel_case,
                       UNICODE,
                       urlencode)

from .tokenizer import (NewickEventFactory, NewickEvents,
                        NewickTokenizer, NewickTokenType)

__all__ = ['input_output', 'str_util', 'dict_wrapper', 'test', 'tokenizer',
           # from input_output
           'download',
           'expand_path', 'expand_to_abspath',
           'open_for_group_write',
           'parse_study_tree_list', 'pretty_dict_str',
           'read_as_json', 'read_filepath',
           'write_to_filepath', 'write_as_json', 'write_pretty_dict_str',
           # from str_util
           'flush_utf_8_writer', 'get_utf_8_string_io_writer',
           'increment_slug', 'is_int_type', 'is_str_type',
           'primitive_string_types',
           'reverse_dict',
           'slugify', 'StringIO',
           'underscored2camel_case', 'UNICODE', 'urlencode',
           # from tokenizer
           'NewickEventFactory', 'NewickEvents',
           'NewickTokenizer', 'NewickTokenType',
           ]
