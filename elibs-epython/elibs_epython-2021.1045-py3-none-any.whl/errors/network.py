# -*- coding: utf-8 -*-
"""
Description:
    Holds the exceptions for the nework module

Author:
    Ray Gomez

Date:
    3/22/21
"""

from epython.errors.base import EPythonException


class EConnectivityException(EPythonException):
    """ Connectivity exception. """


class EInvalidPortState(EPythonException):
    """ Invalid port state exception. """
