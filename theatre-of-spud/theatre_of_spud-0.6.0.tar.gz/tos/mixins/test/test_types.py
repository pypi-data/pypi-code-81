#!/usr/bin/env python3
# encoding: utf-8

# This is a technical demo and teaching example for the turberfield-catchphrase library.
# Copyright (C) 2021 D E Haynes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest

from tos.mixins.types import Material


class MaterialTests(unittest.TestCase):

    def test_simple(self):
        a = Material().set_state(1)
        b = Material(a).set_state(2)
        self.assertEqual(1, b.state)
        self.assertIs(a, a.parent)
        self.assertIs(a, b.parent)

        b.state = 3
        self.assertEqual(1, b.state)
        b.parent = b
        self.assertEqual(3, b.state)
