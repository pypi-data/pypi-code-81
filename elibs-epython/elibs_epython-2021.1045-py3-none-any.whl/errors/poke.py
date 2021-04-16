# -*- coding: utf-8 -*-
"""
Description:
    Drop in replacement wrappers for requests.{GET, POST, PUT, DELETE}

Author:
    Ray Gomez

Date:
    3/16/21
"""

from epython.errors.base import EPythonException


class PokeException(EPythonException):
    """ Raise when an exception occurs establishing a hook. """


class JsonProcessorException(PokeException):
    """ Raise when an exception occurs during JSON Processing. """
