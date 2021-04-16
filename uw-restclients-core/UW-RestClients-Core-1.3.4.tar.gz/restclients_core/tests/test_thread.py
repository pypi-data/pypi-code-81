# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from commonconf import settings, override_settings
from restclients_core.thread import is_django_mysql


class TestThread(TestCase):
    def test_is_django_mysql(self):
        with override_settings(DATABASES=None):
            self.assertFalse(is_django_mysql())

        with override_settings(DATABASES='mysql'):
            self.assertFalse(is_django_mysql())

        with override_settings(
                DATABASES={'default': {
                    'ENGINE': 'django.db.backends.sqlite3'}}):
            self.assertFalse(is_django_mysql())

        with override_settings(
                DATABASES={'default': {
                    'ENGINE': 'django.db.backends.mysql'}}):
            self.assertTrue(is_django_mysql())
