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

from collections import namedtuple
import enum
import random

from turberfield.catchphrase.drama import Drama


class Knowledge:

    Noun = namedtuple("Noun", ["name", "gender"])
    Message = namedtuple(
        "Message", ["attribution", "nouns", "intends", "implies", "tags"]
    )

    @staticmethod
    def implications(msg):
        yield from (i.format(**msg._asdict()) for i in msg.implies)

    @staticmethod
    def intentions(msg):
        yield from (i.format(**msg._asdict()) for i in msg.intends)

    @staticmethod
    def report(msg, n=None):
        attr = msg.attribution
        lookup = {"f": "she", "m": "he", "n": "they"}.get(attr.gender, "it")
        msg = msg._replace(attribution=attr._replace(name=lookup))
        for i in Knowledge.intentions(msg):
            yield f"{attr.name} says {i}"
