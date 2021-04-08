#!/usr/bin/env python3
# encoding: utf-8

# This is a parser-based, web-enabled narrative.
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

from collections import deque
import unittest

from tos.mixins.types import Artifact
from tos.mixins.types import Significance
from tos.mixins.types import Proximity
from tos.mixins.telegraph import Telegraph


class TestTelegraph(unittest.TestCase):

    def setUp(self):
        self.drama = Telegraph()

    def test_modes(self):
        a = Artifact(names=["joke book"])
        b = Artifact(names=["news channel"])
        self.drama.messengers = [
            Telegraph.Messenger(a, ["englishman", "irishman", "scotsman"], 4, period=1),
            Telegraph.Messenger(b, deque(["headlines", "weather", "sport"]), 0, period=3)
        ]
        for n in range(28):
            with self.subTest(n=n, m=self.drama.messengers):
                metadata = self.drama.interlude(None, None)
                if n == 0:
                    self.assertEqual(2, len(self.drama.messengers))
                    self.assertEqual(Significance.notknown, a.get_state(Significance))
                    self.assertEqual(Significance.indicate, b.get_state(Significance))
                    self.assertEqual("headlines", self.drama.messengers[0].messages[0])
                elif n == 1:
                    self.assertEqual(Significance.notknown, a.get_state(Significance))
                    self.assertEqual(Significance.emphasis, b.get_state(Significance))
                    self.assertEqual("headlines", self.drama.messengers[0].messages[0])
                    b.state = Significance.accepted
                elif n == 2:
                    self.assertEqual(Significance.notknown, a.get_state(Significance))
                    self.assertEqual(Significance.inactive, b.get_state(Significance))
                    self.assertEqual("weather", self.drama.messengers[1].messages[0])
                elif n == 4:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual(Significance.inactive, b.get_state(Significance))
                    self.assertEqual("weather", self.drama.messengers[1].messages[0])
                elif n == 5:
                    self.assertEqual(Significance.emphasis, a.get_state(Significance))
                    self.assertEqual(Significance.inactive, b.get_state(Significance))
                    self.assertEqual("englishman", self.drama.messengers[0].messages[0])
                    a.state = Significance.accepted
                    b.state = Significance.accepted
                elif n == 6:
                    self.assertEqual(Significance.inactive, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[0].messages[0])
                elif n == 7:
                    self.assertEqual(Significance.inactive, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[0].messages[0])
                elif n == 8:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[0].messages[0])
                    a.state = Significance.declined
                elif n == 9:
                    self.assertEqual(Significance.inactive, a.get_state(Significance))
                    self.assertEqual("irishman", self.drama.messengers[0].messages[0])
                elif n == 10:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual(Significance.indicate, b.get_state(Significance))
                    self.assertEqual("sport", self.drama.messengers[1].messages[0])
                    self.assertEqual("irishman", self.drama.messengers[0].messages[0])
                    a.state = Significance.accepted
                    b.state = Significance.accepted
                elif n == 11:
                    self.assertEqual(Significance.inactive, a.get_state(Significance))
                    self.assertEqual("scotsman", self.drama.messengers[0].messages[0])
                elif n == 12:
                    self.assertEqual(Significance.inactive, a.get_state(Significance))
                    self.assertEqual("scotsman", self.drama.messengers[0].messages[0])
                elif n == 13:
                    self.assertEqual(Significance.indicate, a.get_state(Significance))
                    self.assertEqual("scotsman", self.drama.messengers[0].messages[0])
                    a.state = Significance.accepted
                elif n == 15:
                    self.assertEqual(Significance.indicate, b.get_state(Significance))
                    self.assertEqual("headlines", self.drama.messengers[0].messages[0])
                    self.assertEqual(1, len(self.drama.messengers))
