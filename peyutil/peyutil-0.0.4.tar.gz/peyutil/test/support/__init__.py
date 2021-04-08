#! /usr/bin/env python
"""Utilities for writing terser tests."""
from .struct_diff import DictDiff


def raise_http_error_with_more_detail(err):
    """Raises string with err.response.text as a ValueError details."""
    # show more useful information (JSON payload) from the server
    details = err.response.text
    raise ValueError("{e}, details: {m}".format(e=err, m=details))


__all__ = ['DictDiff', 'helper',
           'pathmap', 'raise_http_error_with_more_detail', 'struct_diff',
           ]
