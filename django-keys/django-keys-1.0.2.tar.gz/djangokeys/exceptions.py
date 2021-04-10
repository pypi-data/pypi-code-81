#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file contains all exceptions raised by this package.


class DjangoKeysException(Exception):
    """ Base class for any exception raised by this package.
    """
    pass


class KeyNotFound(DjangoKeysException):
    """ File containing key could not be found in strict mode.
    """
    pass


class KeyNotGenerated(DjangoKeysException):
    """ File containing key could not be generated in lax mode.
    """
    pass


class CouldNotAccessKey(DjangoKeysException):
    """ File containing key could not be accessed (read/write).
    """
    pass


class FileDoesNotExist(DjangoKeysException):
    """ File does not exist.
    """
    pass


class EnvironmentVariableNotFound(DjangoKeysException):
    """ Environment variable with a given name was not set by execution
        environment or the loaded .env file.
    """
    pass


class ValueIsEmpty(DjangoKeysException):
    """
    """
    pass


class ValueTypeMismatch(DjangoKeysException):
    """ Value of environment variable cannot be interpreted as expected type.
    """
    pass


class CouldNotCreateFile(DjangoKeysException):
    """ Could not create a new file.
    """
    pass
