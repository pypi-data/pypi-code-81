#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for accessing environment variables as an int.

import pytest

from djangokeys.djangokeys import DjangoKeys
from djangokeys.exceptions import EnvironmentVariableNotFound
from djangokeys.exceptions import ValueIsEmpty
from djangokeys.exceptions import ValueTypeMismatch

from tests.files import DJANGOKEYS_ACCESSING_TYPES_ENV_PATH


def test__django_keys_int__not_found():
    """ An appropriate exception is raised when env var is not set.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(EnvironmentVariableNotFound):
        keys.int("DOES_NOT_EXIST")


def test__django_keys_int__empty():
    """ An empty value cannot be interpreted as an int.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueIsEmpty):
        keys.int("EMPTY_VALUE")


def test__django_keys_int_regular_int():
    """ A regular integer is interpreted as an int.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.int("INT_VALUE") == 5


def test__django_keys_int__float():
    """ A float value cannot be interpreted as an int.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueTypeMismatch):
        keys.int("INT_VALUE_FLOAT")


def test__django_keys_int__random_characters():
    """ A random string of characters cannot be interpreted as an int.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(ValueTypeMismatch):
        keys.int("INT_VALUE_INVALID")
