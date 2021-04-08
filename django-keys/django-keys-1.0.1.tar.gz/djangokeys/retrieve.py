#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file contains the functionality for generating secret keys in django.

import os

from .generate import generate_django_key
from .exceptions import KeyNotFound
from .exceptions import KeyNotGenerated
from .exceptions import CouldNotAccessKey


def retrieve_key_from_file(filepath, *, strict=False):
    """ Attempts to retrieve a key from the file with the given filepath.

    If in strict mode, and the file is not found, an exception is raised.

    If not in strict mode, and the file is not found, a new key is generated
    and stored in a file at the expected location.

    :param str filepath: filepath of file in which key is stored
    :param bool strict: assert that file already exists (default: False)

    :raises KeyNotFound: file containing key not found in strict mode
    :raises KeyNotGenerated: file containing key not generated in lax mode
    :raises CouldNotAccessKey: could not retrieve key from file

    :returns secret django key stored in file
    :rtype: str
    """
    if not os.path.isfile(filepath) and strict:
        raise KeyNotFound("Could not find file in strict mode.")
    if not os.path.isfile(filepath) and not strict:
        key = generate_django_key()
        _write_key_to_file(filepath, key)
    return _read_key_from_file(filepath)


def _write_key_to_file(filepath, key):
    """ Attempts to write generated key to file.
    """
    try:
        with open(filepath, 'w') as f:
            _write_to_file(f, key)
    except (IOError, OSError):
        raise KeyNotGenerated("Unable to write generated key to file.")


def _read_key_from_file(filepath):
    """ Attempts to retrieve key from file.
    """
    try:
        with open(filepath, 'r') as f:
            key = _read_from_file(f)
    except (IOError, OSError):
        raise CouldNotAccessKey("Unable to retrieve key from file.")
    return key


def _write_to_file(f, t):
    """ Write text to open file.
    """
    f.write(t)


def _read_from_file(f):
    """ Read text from file.
    """
    return f.read()
