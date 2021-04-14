#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This module contains all exceptions that can be raised by this package.


class HanjaqException(Exception):
    """ Base class for all exceptions that can be raised by this package.
    """
    pass


class NotASingleCharacter(HanjaqException):
    """ Expected a single character as string with length one.
    """
    pass


class NotAHanjaCharacter(HanjaqException):
    """ Expected a Hanja character as a string with length one.
    """
    pass


class DictionaryProblem(HanjaqException):
    """ Signals a problem with contents of hanja.txt file.
    """
    pass
