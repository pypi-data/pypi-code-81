#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for accessing environment variables as a float.

import pytest

from djangokeys.djangokeys import DjangoKeys
from djangokeys.exceptions import EnvironmentVariableNotFound
from djangokeys.exceptions import ValueIsEmpty
from djangokeys.exceptions import ValueTypeMismatch

from tests.files import DJANGOKEYS_ACCESSING_TYPES_ENV_PATH


def test__django_keys_float__not_found():
    """ An appropriate exception is raised when env var is not set.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(EnvironmentVariableNotFound):
        keys.float("DOES_NOT_EXIST")


def test__django_keys_float__empty():
    """ An empty value cannot be interpreted as a float.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueIsEmpty):
        keys.float("EMPTY_VALUE")


def test__django_keys_float__regular():
    """ A regular float can be interpreted as a float.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.float("FLOAT_VALUE")


def test__django_keys_float__int():
    """ A regular int can be interpreted as a float.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.float("FLOAT_VALUE_INT")


def test__django_keys_float__invalid():
    """ A random string of characters cannot be interpreted as a float.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueTypeMismatch):
        keys.float("FLOAT_VALUE_INVALID")
