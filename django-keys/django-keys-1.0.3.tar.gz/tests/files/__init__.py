#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains paths to local files of this submodule.

import os


# path of directory containing files
_FILES_DIR = os.path.dirname(os.path.realpath(__file__))

# path to simple example of .env file
EXAMPLE1_ENV_PATH = os.path.join(_FILES_DIR, "example1.env")

# path to empty .env file
EMPTY_ENV_PATH = os.path.join(_FILES_DIR, "empty.env")

# path to .env file used for testing overwriting values of env vars
DJANGOKEYS_OVERWRITING_ENV_PATH = \
    os.path.join(_FILES_DIR, "djangokeys_overwriting.env")

# path to .env file used for testing accessing values of env vars
DJANGOKEYS_ACCESSING_TYPES_ENV_PATH = \
    os.path.join(_FILES_DIR, "djangokeys_accessing_types.env")
