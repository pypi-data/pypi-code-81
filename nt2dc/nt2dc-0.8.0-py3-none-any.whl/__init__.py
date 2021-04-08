#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of nt2dc
# (see https://github.com/carstencodes/nt2dc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#
"""This module provides methods to convert a named tuple to a data class.
   There is also a set of methods to convert a dataclass back to namedtuple,
   if needed.
"""

from .named_tuple import make_dataclass, get_dataclass_object
from .dataclass import namedtuple, get_named_tuple_object

__all__ = [
    "make_dataclass",
    "get_dataclass_object",
    "namedtuple",
    "get_named_tuple_object",
]
