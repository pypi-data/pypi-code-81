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
"""
    MusaMusa-ETR project : musamusa_etr/utils.py

    various utilities

    ____________________________________________________________________________


    o path_of()           : return the path to a file
"""
import os.path


def path_of(filename):
    """
        path_of()

        Return the path to <filename>
        ______________________________________________________________________


        o filename : (str) the source filename (i.e. =path + read filename)

        RETURNED VALUE : (str)the path contained in <filename>
    """
    return os.path.split(filename)[0]
