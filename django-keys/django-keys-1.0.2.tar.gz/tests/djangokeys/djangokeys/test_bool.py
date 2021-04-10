#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for accessing environment variables as a bool.

import pytest

from djangokeys.djangokeys import DjangoKeys
from djangokeys.exceptions import EnvironmentVariableNotFound
from djangokeys.exceptions import ValueIsEmpty
from djangokeys.exceptions import ValueTypeMismatch

from tests.files import DJANGOKEYS_ACCESSING_TYPES_ENV_PATH


def test__django_keys_bool__not_found():
    """ An appropriate exception is raised when env var is not set.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(EnvironmentVariableNotFound):
        keys.bool("DOES_NOT_EXIST")


def test__django_keys_bool__empty():
    """ An empty value cannot be interpreted as a bool.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueIsEmpty):
        keys.bool("EMPTY_VALUE")


def test__django_keys_bool__regular_true():
    """ 'True' is interpreted correctly.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.bool("BOOL_VALUE_TRUE")


def test__django_keys_bool__regular_false():
    """ 'False' is interpreted correctly.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert not keys.bool("BOOL_VALUE_FALSE")


def test__django_keys_bool__alternative_true_values():
    """ Alternative values of True are interpreted correctly.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.bool("BOOL_VALUE_TRUE_T")
    assert keys.bool("BOOL_VALUE_TRUE_1")
    assert keys.bool("BOOL_VALUE_TRUE_Y")
    assert keys.bool("BOOL_VALUE_TRUE_YES")


def test__django_keys_bool__alternative_false_values():
    """ Alternative values of False are interpreted correctly.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert not keys.bool("BOOL_VALUE_FALSE_F")
    assert not keys.bool("BOOL_VALUE_FALSE_0")
    assert not keys.bool("BOOL_VALUE_FALSE_N")
    assert not keys.bool("BOOL_VALUE_FALSE_NO")


def test__django_keys_bool__invalid():
    """ A random string of characters cannot be interpreted as a bool.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueTypeMismatch):
        keys.bool("BOOL_VALUE_INVALID")
