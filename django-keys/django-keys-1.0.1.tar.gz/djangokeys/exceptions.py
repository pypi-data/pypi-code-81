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
