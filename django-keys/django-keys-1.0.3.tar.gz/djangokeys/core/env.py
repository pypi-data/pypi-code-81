#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains functionality to read values from .env files.

import os
import dotenv


def read_values_from_env(filepath):
    """ Reads environment variables from .env file with a given path.

    :param str filepath: path of file
    :return: dictionary containing key-value pairs listed in file
    :rtype: dict
    """
    if not os.path.exists(filepath):
        # TODO: inform that .env file did not exist
        return dict()
    return dotenv.dotenv_values(filepath)
