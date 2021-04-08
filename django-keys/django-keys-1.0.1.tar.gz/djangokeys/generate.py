#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file contains the functionality for generating secret keys in django.

import secrets

from .settings import DJANGO_DEFAULT_KEY_LENGTH as DEFAULT_LENGTH
from .settings import DJANGO_DEFAULT_SYMBOLS as DEFAULT_SYMBOLS


def generate_django_key(*, key_length=DEFAULT_LENGTH, symbols=DEFAULT_SYMBOLS):
    """ Generates a new secret key that is conform with Django's standard.

    :param int key_length: length of generated keys (optional)
    :param str symbols: string of symbols that key is composed of (optional)

    :return: a newly generated secret key
    :rtype: str
    """
    return "".join([secrets.choice(symbols) for _ in range(key_length)])
