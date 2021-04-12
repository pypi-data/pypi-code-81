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
   MusaMusa-TextRef project : musamusa_textref/subref.py

   The SubRef class is an internal class used by TextRef* classes.


   (pimydoc)about textual references
   ⋅ References to a text are a way to locate an excerpt in a longer text.
   ⋅
   ⋅ For the user, a textual reference (=textref) is a string describing one
   ⋅ or more references:
   ⋅
   ⋅         By example. "Beowulf.43a-Beowulf.44b" means
   ⋅                     Beowulf.43a+Beowulf.43b+Beowulf.44a+Beowulf.44b
   ⋅
   ⋅ Under the hood, three levels of references are distinguished:
   ⋅
   ⋅     - mono-textref like "Beowulf.43a"
   ⋅         > "Beowulf.43a" means nothing but "Beowulf.43a"
   ⋅     - bi-textref like "Beowulf.43a" or "Beowulf.43a-Beowulf.44b"
   ⋅         > "Beowulf.43a-Beowulf.44b" means
   ⋅           Beowulf.43a+Beowulf.43b+Beowulf.44a+Beowulf.44b
   ⋅     - multi-textref like "Beowulf.43a-", "Beowulf.43a-Beowulf.44b"
   ⋅       or "Beowulf.43a-Beowulf.44b;Beowulf.43c"
   ⋅         > "Beowulf.43a-Beowulf.44b;Beowulf.43c" means
   ⋅           Beowulf.43a+Beowulf.43b+Beowulf.44a+Beowulf.44b+Beowulf.43c

   (pimydoc)monoref/biref/multiref(internal)
   ⋅ Internal representation of mono-/bi-/multi- textref:
   ⋅
   ⋅     o  mono textref: "Beowulf.3" is internally stored as:
   ⋅
   ⋅                     ((None, 'Beowulf'), ('int', 3))
   ⋅                       ^     ^             ^     ^
   ⋅                       ^     ^             ^     value (here, a int)
   ⋅                       ^     ^             ^
   ⋅                       ^     ^             [0] : value type
   ⋅                       ^     ^
   ⋅                       ^     [1]value : since [0] is None, it's a string.
   ⋅                       ^
   ⋅                       [0] is None if the value (here 'Beowulf') is not countable
   ⋅
   ⋅     o  bi textref: "Beowulf.3-Beowulf.4" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      ((None, 'Beowulf'), ('int', 3)),
   ⋅                      ((None, 'Beowulf'), ('int', 4))
   ⋅                     )
   ⋅
   ⋅                     "Beowulf.3-" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      ((None, 'Beowulf'), ('int', 3)),
   ⋅                     )
   ⋅
   ⋅     o  multi textrefs: "Beowulf.3-Beowulf.4;Beowulf.7" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      (((None, 'Beowulf'), ('int', 3)),
   ⋅                       ((None, 'Beowulf'), ('int', 4))
   ⋅                      ),
   ⋅                      (((None, 'Beowulf'), ('int', 7)),
   ⋅                      ),
   ⋅                     )
   ⋅
   ⋅ To get lists-/tuples- only definitions, use
   ⋅     TextRefBaseClass._definition_as_lists() and
   ⋅     TextRefBaseClass._definition_as_tuples()
   ⋅     methods

   ____________________________________________________________________________

   class:

   o  SubRef class
"""
# NamedTuple is a class, even if pylint thinks otherwise.
# pylint: disable=inherit-non-class

# SubRef being a NamedTuple class, it's normal it has no public method.
# pylint: disable=too-few-public-methods

from typing import NamedTuple


class SubRef(NamedTuple):
    """
        SubRef class

        Type used by TextRefBaseClass._subrefs

        (pimydoc)TextRefBaseClass._subrefs structure
        ⋅ TextRefBaseClass._subref is a tuple made of:
        ⋅
        ⋅     *  .regex     : (bytes)a compiled regex
        ⋅     *  .min_value : None or (integer) minimal value
        ⋅     *  .max_value : None or (integer) maximal value
        ⋅     *  .char2int  : None or (a dict)  character to integer value
        ⋅
        ⋅     By example:
        ⋅     * re.compile(r"^[a-z]$"),
        ⋅     * 1,
        ⋅     * 26,
        ⋅     * {"a": 1,
        ⋅        "b": 2,
        ⋅        ...
        ⋅        "z": 26}
    """
    regex: bytes
    min_value: int
    max_value: int
    char2int: dict
