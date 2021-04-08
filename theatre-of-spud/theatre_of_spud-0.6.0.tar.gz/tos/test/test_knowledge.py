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

from tos.knowledge import Knowledge


class KnowledgeTests(unittest.TestCase):

    def setUp(self):
        self.msg = Knowledge.Message(
            Knowledge.Noun("Angela", "f"), (Knowledge.Noun("Bobby", "m"),),
            ("{attribution.name} is taking {nouns[0].name} to the {tags[0]} in {tags[1]}",
             "{attribution.name} has to take {nouns[0].name} to the {tags[0]} in {tags[1]}"),
            ("{attribution.name} is at the {tags[0]}", "{attribution.name} is in {tags[1]}",
             "{nouns[0].name} is at the {tags[0]}", "{nouns[0].name} is in {tags[1]}"),
            ("caravan", "Minehead")
        )

    def test_implications(self):
        check = "Bobby is in Minehead"
        self.assertEqual(check, list(Knowledge.implications(self.msg))[3])

    def test_intentions(self):
        check = "Angela is taking Bobby to the caravan in Minehead"
        self.assertEqual(check, list(Knowledge.intentions(self.msg))[0])

    def test_report(self):
        report = "Angela says she has to take Bobby to the caravan in Minehead"
        self.assertEqual(report, list(Knowledge.report(self.msg))[1])
