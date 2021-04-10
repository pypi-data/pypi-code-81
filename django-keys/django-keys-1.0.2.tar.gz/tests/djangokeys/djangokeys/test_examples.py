#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for djangokeys submodule.

from djangokeys.djangokeys import DjangoKeys

from tests.files import EXAMPLE1_ENV_PATH


def test__django_keys__initialization():
    """ Tests that DjangoKeys instance is constructed correctly.
    """
    keys = DjangoKeys(EXAMPLE1_ENV_PATH)
    assert keys.str("DOMAIN") == "example.org"
    assert keys.str("ADMIN_EMAIL") == "admin@example.org"
    assert keys.str("ROOT_URL") == "example.org/app"
    assert keys.str("HELLO") == "nobody answers back"
