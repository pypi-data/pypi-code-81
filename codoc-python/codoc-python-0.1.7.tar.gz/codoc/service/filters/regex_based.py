#!/usr/bin/env python3
import re

from .high_order_filter import filter_nodes_by_lambda
from .types import FilterType


def filter_by_regex(pattern: str, flags=0) -> FilterType:
    """
    This allows you to filter nodes based on whether they fulfill
    some regex query. This is ideal if you, for instance, want to remove all
    test related things.

    The regex is done solely on the `name` attribute.

    The following example removes all instances of "test".
    Example:
       graph = filters.filter_by_regex("test", flags=re.IGNORECASE)(graph)

    To understand how to use regex, please consult the python documentation:

    https://docs.python.org/3/library/re.html
    """

    pattern = re.compile(pattern, flags=flags)
    return filter_nodes_by_lambda(lambda node: pattern.search(node.name) is not None)


def exclude_by_regex(pattern: str, flags=0) -> FilterType:
    """
    This allows you to filter nodes based on whether they fulfill
    some regex query. This is ideal if you, for instance, want to remove all
    test related things.

    The regex is done solely on the `name` attribute.

    The following example removes all instances of "test".
    Example:
       graph = filters.filter_by_regex("test", flags=re.IGNORECASE)(graph)

    To understand how to use regex, please consult the python documentation:

    https://docs.python.org/3/library/re.html
    """

    pattern = re.compile(pattern, flags=flags)
    return filter_nodes_by_lambda(lambda node: pattern.search(node.name) is None)
