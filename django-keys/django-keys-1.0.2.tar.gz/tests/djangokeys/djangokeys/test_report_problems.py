#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains tests for reporting potential problems.

from djangokeys.djangokeys import DjangoKeys

from tests.files import EMPTY_ENV_PATH


def test__django_keys_report_problems():
    """ placeholder
    """
    keys = DjangoKeys(EMPTY_ENV_PATH)
    keys.report_problems()  # this method does nothing yet
