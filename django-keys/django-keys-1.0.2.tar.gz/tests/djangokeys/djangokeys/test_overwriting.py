#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for overwriting environment variables set by exec env.

from djangokeys.djangokeys import DjangoKeys

from tests.files import DJANGOKEYS_OVERWRITING_ENV_PATH
from tests.utils.environment_vars import use_environment_variable


def test__django_keys__overwriting_env_variables__disallowed():
    """ If overwrite=False, environment variable cannot be overwritten by .env.
    """
    with use_environment_variable('MY_EXAMPLE_VAR_6274', 'original'):
        keys = DjangoKeys(DJANGOKEYS_OVERWRITING_ENV_PATH)
        assert keys.str('MY_EXAMPLE_VAR_6274', overwrite=False) == "original"


def test__django_keys__overwriting_env_variables__allowed():
    """ If overwrite=True, environment variable can be overwritten by .env.
    """
    with use_environment_variable('MY_EXAMPLE_VAR_6274', 'original'):
        keys = DjangoKeys(DJANGOKEYS_OVERWRITING_ENV_PATH)
        assert keys.str('MY_EXAMPLE_VAR_6274', overwrite=True) == "overwritten"
