#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains functionality related to modules.

import importlib.machinery
import os
import sys


def resolve_module_path(module_name):
    """ Returns absolute filepath of Python module with a given name.

    :param str module_name: qualified name used to import module
    """
    # Python's built-in functionality does not allow us to resolve the
    # filepath of "deeper" submodules directly, hence the stepwise approach.
    finder = importlib.machinery.PathFinder()
    search_path = sys.path
    search_result = None
    for submodule_name in module_name.split("."):
        module = finder.find_spec(submodule_name, path=search_path)
        if not module:
            return None
        search_result = os.path.realpath(module.origin)
        search_path = [os.path.dirname(search_result)]
    return search_result
