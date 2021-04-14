#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for mapping module names to filepaths.

import djangokeys.utils.modules as m


def test__resolve_module_path__exists():
    """ Absolute path is returned if module is found.
    """
    path = m.resolve_module_path('tests.djangokeys.utils.test_modules')
    assert path == __file__


def test__resolve_module_path__doesnt_exist():
    """ None is returned if the module could not be found.
    """
    path = m.resolve_module_path('does.not.exist')
    assert path is None


def test__resolve_module_path__partially_doesnt_exist():
    """ None is returned when the search wrong at some point.
    """
    path = m.resolve_module_path('tests.djangokeys.does.not.exist')
    assert path is None


def test__resolve_module_path__empty():
    """ None is returned if the module argument is an empty string.
    """
    path = m.resolve_module_path('')
    assert path is None
