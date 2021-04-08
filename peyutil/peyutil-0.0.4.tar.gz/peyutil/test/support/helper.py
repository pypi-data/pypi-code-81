#!/usr/bin/env python
"""A few utility functions for making tests terser."""

import codecs
import json
from peyutil.str_util import is_str_type


def testing_read_json(fp):
    """Reads a UTF-8 JSON from filepath."""
    with codecs.open(fp, 'r', encoding='utf-8') as f:
        return json.load(f)


def testing_write_json(o, fp):
    """Writes a UTF-8 JSON to filepath."""
    with codecs.open(fp, 'w', encoding='utf-8') as fo:
        json.dump(o, fo, indent=2, sort_keys=True)
        fo.write('\n')


def testing_through_json(d):
    """Returns a deserialized version of the JSON serialization of `d`."""
    return json.loads(json.dumps(d))


def testing_dict_eq(a, b):
    """You should just call a == b. This is a legacy of a verbose dict compare."""
    return a == b


def testing_conv_key_unicode_literal(d):
    """Not intended for widespread use. Used in some NexSON tests."""
    r = {}
    if not isinstance(d, dict):
        return d
    for k, v in d.items():
        if isinstance(v, dict):
            r[k] = testing_conv_key_unicode_literal(v)
        elif isinstance(v, list):
            r[k] = [testing_conv_key_unicode_literal(i) for i in v]
        elif is_str_type(v) and v == 'unicode':
            r[k] = 'str'
        else:
            r[k] = v
    return r
