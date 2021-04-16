#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: ynabinterfaceslib.py
#
# Copyright 2019 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for ynabinterfaceslib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import abc
import logging
from collections import OrderedDict

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''16-08-2019'''
__copyright__ = '''Copyright 2019, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<costas.tyf@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''ynabinterfaceslib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Comparable(abc.ABC):
    """Interface for something that can be comparable based on a _data internal attribute."""

    def __init__(self, data):
        self._logger = logging.getLogger(f'{LOGGER_BASENAME}.{self.__class__.__name__}')
        self._data = data

    @property
    def _comparable_attributes(self):
        pass

    @property
    def _comparable_data(self):
        return OrderedDict({key: getattr(self, key) for key in self._comparable_attributes})

    def __hash__(self):
        return hash(str(self._comparable_data))

    def __eq__(self, other):
        """Override the default equals behavior."""
        if not isinstance(other, Comparable):
            raise ValueError('Not a Comparable object')
        return hash(self) == hash(other)

    def __ne__(self, other):
        """Override the default unequal behavior."""
        if not isinstance(other, Comparable):
            raise ValueError('Not a Comparable object')
        return hash(self) != hash(other)


class Transaction(Comparable):  # pylint: disable=too-few-public-methods
    """Interface for a transaction object."""

    @staticmethod
    def _clean_up(string):
        return " ".join(string.split()).replace('\x00', '')


class Contract(abc.ABC):  # pylint: disable=too-few-public-methods
    """Interface for a bank contract giving access to accounts."""

    @abc.abstractmethod
    def get_account(self, id_):
        """Should implement an easy account retrieval by provided ID.

        ID could be either IBAN for bank accounts, or account numbers for credit cards.

        In case of single accounts in contract should be implemented to return the only account
        even with no argument provided.
        """
