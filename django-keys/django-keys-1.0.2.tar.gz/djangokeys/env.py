#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains functionality to read values from .env files.

import os
import dotenv

from djangokeys.exceptions import FileDoesNotExist


def read_values_from_env(filepath):
    """ Reads environment variables from .env file with a given path.

    :param str filepath: path of file
    :return: dictionary containing key-value pairs listed in file
    :rtype: dict
    """
    if not os.path.exists(filepath):
        msg = "Could not read environment variables from '{}'."
        raise FileDoesNotExist(msg.format(filepath))
    return dotenv.dotenv_values(filepath)
