#!/usr/bin/env python

# This tool conjugates Galician verbs and can add them enclitic pronouns.
# Copyright (C) 2020 Andrés Vieites Pérez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .conjugation import conjugate
from .load_paradigms import TENSES_KEY, FN_KEY, PI_KEY, II_KEY, \
                            IA_KEY, IP_KEY, EI_KEY, MI_KEY, TI_KEY, FI_KEY, \
                            PS_KEY, IS_KEY, FS_KEY, IN_KEY
