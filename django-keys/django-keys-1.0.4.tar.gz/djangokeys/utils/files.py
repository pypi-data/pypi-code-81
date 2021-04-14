#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains functionality to interact with files.

from os.path import exists

from djangokeys.exceptions import CouldNotCreateFile


def touch_file(path):
    """ Creates a new file with a given path if the file doesn't exist yet.
        Nothing happens if the file already exists.

    :param str path: path of file
    :raises CouldNotCreateFile: file could not be created
    """
    if exists(path):
        return
    try:
        open(path, 'w').close()
    except IOError:
        msg = "Could not create a new file: {}"
        raise CouldNotCreateFile(msg.format(path))
