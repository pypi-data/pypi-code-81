#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for accessing env vars that aren't listed in .env.

from djangokeys.djangokeys import DjangoKeys

from tests.files import EMPTY_ENV_PATH
from tests.utils.environment_vars import use_environment_variable


def test__django_keys__overwriting_env_variables__disallowed():
    """ If overwrite=False, environment variable cannot be overwritten by .env.
    """
    with use_environment_variable('DK_TEST_KEY', 'value'):
        keys = DjangoKeys(EMPTY_ENV_PATH)
        assert keys.str('DK_TEST_KEY') == "value"
