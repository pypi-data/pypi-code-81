#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-ETR Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-ETR.
#    MusaMusa-ETR is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-ETR is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-ETR.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
r"""
   MusaMusa-ETR project : musamusa_etr/etr_line.py

   ETRLine class and related constants

   ____________________________________________________________________________

   CONSTANTS:
   o  ETRLINE_INTTYPE__NORMAL
   o  ETRLINE_INTTYPE__COMMENTEMPTY
   o  ETRLINE_INTTYPE__PARSINGTOOLSDEFINITION
   o  ETRLINE_INTTYPE__VARIABLE
   o  ETRLINE_INTTYPE__TAG
   o  ETRLINE_INTTYPE__NONE

   CLASSES:
   o  ETRLine class
   o  TLFF class
"""
from dataclasses import dataclass

ETRLINE_INTTYPE__NORMAL = 0
ETRLINE_INTTYPE__COMMENTEMPTY = 1
ETRLINE_INTTYPE__PARSINGTOOLSDEFINITION = 2
ETRLINE_INTTYPE__VARIABLE = 3
ETRLINE_INTTYPE__TAG = 4
ETRLINE_INTTYPE__NONE = 99


# ETRLine could indeed almost be a dataclass.
# pylint: disable=too-few-public-methods
class ETRLine:
    """
        ETRLine class

        Object yielded by ETR.read()
        _______________________________________________________________________

        ATTRIBUTES:
        o (str)line
        o (tuple of FileAndLine objects)fals
        o (tuple of strings)flags
            (pimydoc)flags
            ⋅Flags are sorted alphabetically via the sorted() function.
            ⋅In fine, flags must be a tuple of strings : they can't be None.
        o (int)line_inttype
    """
    def __init__(self,
                 line,
                 fals=None,
                 flags=None,
                 line_inttype=ETRLINE_INTTYPE__NORMAL):
        """
            ETRLine.__init__()
            __________________________________________________________________

            ARGUMENTS:
            o  (str)line             : the line that has been read
            o  (int)line_inttype     : (int) ETRLINE_xxx constant
            o  (None|list of FAL)fals: the FALs objects associated to the <line>.
            o  (None|tuple)flags     : None or a list of str.
                   (pimydoc)flags
                   ⋅Flags are sorted alphabetically via the sorted() function.
                   ⋅In fine, flags must be a tuple of strings : they can't be None.
        """
        self.line = line

        if fals is None:
            self.fals = tuple()
        else:
            self.fals = fals

        if flags is None:
            self.flags = tuple()
        else:
            self.flags = flags

        self.line_inttype = line_inttype

    def __str__(self):
        """
            ETRLine.__str__()
        """
        return f"ETRLine(" \
            f"line='{self.line}', " \
            f"fals={self.fals}, " \
            f"flags={self.flags}, " \
            f"line_inttype={self.line_inttype}" \
            ")"


@dataclass
class TLFF:
    """
        TLFF class

        T[ype] L[ine] F[als] and F[lags]

        Class used to pass some arguments to ETR._read_action*() methods.

        _______________________________________________________________________

        ATTRIBUTES:

        o  (int)line_inttype     : (int) ETRLINE_xxx constant
        o  (None|str)line        : the line that has been read
        o  (None|list of FAL)fals: the FALs objects associated to the <line>.
        o  (None|tuple)flags     : None or a list of str.
    """
    line_inttype: int = ETRLINE_INTTYPE__NONE
    line: str = None
    fals: tuple = None
    flags: tuple = None
