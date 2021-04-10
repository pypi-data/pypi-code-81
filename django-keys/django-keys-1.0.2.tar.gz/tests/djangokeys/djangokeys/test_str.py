#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for accessing environment variables as a str.

import pytest

from djangokeys.djangokeys import DjangoKeys
from djangokeys.exceptions import EnvironmentVariableNotFound

from tests.files import DJANGOKEYS_ACCESSING_TYPES_ENV_PATH


def test__django_keys_str__not_found():
    """ An appropriate exception is raised when env var is not set.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    with pytest.raises(EnvironmentVariableNotFound):
        keys.str("DOES_NOT_EXIST")


def test__django_keys_str__empty_string():
    """ An empty value is interpreted as an empty string.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.str("EMPTY_VALUE") == ""


def test__django_keys_str__regular_string():
    """ A string is interpreted as is.
    """
    keys = DjangoKeys(DJANGOKEYS_ACCESSING_TYPES_ENV_PATH)
    assert keys.str("STR_VALUE") == "helLo WOrld"
