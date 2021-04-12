#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-TextRef Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-TextRef.
#    MusaMusa-TextRef is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-TextRef is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-TextRef.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-TextRef project : musamusa_textref/textrefdefault.py

   Text Reference default class : TextRefDefault

        TextRefDefault is a general purpose class, allowing to read
   complex strings like "AncientTestament.Genesis.IX.3a"


   Unit testing: see tests/textrefdefault.py

   ____________________________________________________________________________

   class:
   o TextRefDefault class
"""
# TextRefDefault DOES have public methods, inherited from TextRefBaseClass.
# pylint: disable=too-few-public-methods
from musamusa_textref.textref import TextRefBaseClass


class TextRefDefault(TextRefBaseClass):
    """
        TextRefBaseClass class
    """
    _refs_separator = ";"
    _ref2ref_separator = "-"
    _refsubpart_separator = "."
