#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains unit tests for functionality related to generating keys.

from djangokeys.generate import generate_django_key
from djangokeys.settings import DJANGO_DEFAULT_KEY_LENGTH
from djangokeys.settings import DJANGO_DEFAULT_SYMBOLS


def test_generate_key():
    """ Test that a key was generated with default key length and symbols.
    """
    k = generate_django_key()
    assert isinstance(k, str)
    assert len(k) == DJANGO_DEFAULT_KEY_LENGTH
    assert all([ch in DJANGO_DEFAULT_SYMBOLS for ch in k])


def test_generate_key_case_different_length():
    """ Test that a key with a specific key length is generated.
    """
    k = generate_django_key(key_length=32)
    assert isinstance(k, str)
    assert len(k) == 32
    assert all([ch in DJANGO_DEFAULT_SYMBOLS for ch in k])


def test_generate_key_case_different_symbols():
    """ Test that a key with different symbols is generated.
    """
    k = generate_django_key(symbols="abcde")
    assert isinstance(k, str)
    assert len(k) == DJANGO_DEFAULT_KEY_LENGTH
    assert all([ch in "abcde" for ch in k])
