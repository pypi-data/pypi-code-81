# -*- coding: utf-8 -*-
"""
Description:
    Holds the exceptions for the filters module

Author:
    Ray Gomez

Date:
    3/22/21
"""

from epython.errors.base import EPythonException


class EFilterException(EPythonException):
    """ Base filter exception. """


class ERegExFilterException(EFilterException):
    """ Filter exception raise for issues with regex. """
