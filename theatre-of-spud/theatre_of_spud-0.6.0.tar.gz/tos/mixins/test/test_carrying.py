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

import unittest

from tos.mixins.types import Artifact
from tos.mixins.types import Character
from tos.mixins.types import Proximity
from tos.mixins.carrying import Carrying

from tos.mixins.test.test_moving import TestTrack


class TestCarrying(unittest.TestCase):

    def setUp(self):
        self.drama = Carrying(TestTrack())

    def test_simple(self):
        p = Character(names=["player"]).set_state(self.drama.nav.Location["1"])
        t = Character(names=["thing"]).set_state(self.drama.nav.Location["4"])
        self.drama.player = p
        self.drama.add(p, t)
        p.state = self.drama.nav.Arriving["4"]

        metadata = self.drama.interlude(None, None)
        locn = p.get_state(self.drama.nav.Location)
        self.assertEqual("2", p.get_state(self.drama.nav.Location).name)
        self.assertEqual(Proximity.distant, t.get_state(Proximity))

        metadata = self.drama.interlude(None, None)
        locn = p.get_state(self.drama.nav.Location)
        self.assertEqual("3", p.get_state(self.drama.nav.Location).name)
        self.assertEqual(Proximity.outside, t.get_state(Proximity))

        metadata = self.drama.interlude(None, None)
        locn = p.get_state(self.drama.nav.Location)
        self.assertEqual("4", p.get_state(self.drama.nav.Location).name)
        self.assertEqual(Proximity.present, t.get_state(Proximity))

        
        dlg = "\n".join(self.drama(self.drama.do_get, "", obj=t))
        self.assertEqual("Now carrying the thing.", dlg)

        p.state = self.drama.nav.Arriving["7"]

        metadata = self.drama.interlude(None, None)
        locn = p.get_state(self.drama.nav.Location)
        self.assertEqual("5", p.get_state(self.drama.nav.Location).name)
        self.assertEqual("5", t.get_state(self.drama.nav.Location).name)
        self.assertEqual(Proximity.carried, t.get_state(Proximity))

        # Drop the thing.
        t.state = Proximity.present

        metadata = self.drama.interlude(None, None)
        locn = p.get_state(self.drama.nav.Location)
        self.assertEqual("6", p.get_state(self.drama.nav.Location).name)
        self.assertEqual("5", t.get_state(self.drama.nav.Location).name)
        self.assertEqual(Proximity.outside, t.get_state(Proximity))

        metadata = self.drama.interlude(None, None)
        locn = p.get_state(self.drama.nav.Location)
        self.assertEqual("7", p.get_state(self.drama.nav.Location).name)
        self.assertEqual("5", t.get_state(self.drama.nav.Location).name)
        self.assertEqual(Proximity.distant, t.get_state(Proximity))
