#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for accessing env vars as Django's secret key.

import pytest

from djangokeys.djangokeys import DjangoKeys
from djangokeys.exceptions import EnvironmentVariableNotFound
from djangokeys.exceptions import ValueIsEmpty

from tests.files import EMPTY_ENV_PATH
from tests.utils.environment_vars import use_environment_variable


def test__django_keys_secret_key__not_found():
    """ An appropriate exception is raised when env var is not set.
    """
    keys = DjangoKeys(EMPTY_ENV_PATH)
    with pytest.raises(EnvironmentVariableNotFound):
        keys.secret_key("DOES_NOT_EXIST")


def test__django_keys_str__empty_string():
    """ An empty value cannot be used as Django's secret key.
    """
    with use_environment_variable('SECRET_KEY', ''):
        keys = DjangoKeys(EMPTY_ENV_PATH)
        with pytest.raises(ValueIsEmpty):
            keys.secret_key('SECRET_KEY')


def test__django_keys_str__regular_string():
    """ A string of characters can be used as Django's secret key.
    """
    with use_environment_variable('SECRET_KEY', 'abcDE12345'):
        keys = DjangoKeys(EMPTY_ENV_PATH)
        assert keys.secret_key("SECRET_KEY") == "abcDE12345"
