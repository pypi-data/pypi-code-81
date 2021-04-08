#!/usr/bin/env python3
#   encoding: utf-8

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

import enum

from turberfield.dialogue.types import EnumFactory


class Motivation(EnumFactory, enum.Enum):

    acting = enum.auto()
    author = enum.auto()
    banker = enum.auto()
    battle = enum.auto()
    boring = enum.auto()
    buying = enum.auto()
    credit = enum.auto()
    critic = enum.auto()
    debtor = enum.auto()
    duress = enum.auto()
    elvish = enum.auto()
    father = enum.auto()
    finish = enum.auto()
    friend = enum.auto()
    grovel = enum.auto()
    herald = enum.auto()
    helper = enum.auto()
    hubris = enum.auto()
    insert = enum.auto()
    joking = enum.auto()
    killer = enum.auto()
    knight = enum.auto()
    leader = enum.auto()
    mother = enum.auto()
    murder = enum.auto()
    nobody = enum.auto()
    prince = enum.auto()
    profit = enum.auto()
    reader = enum.auto()
    vendor = enum.auto()
    victim = enum.auto()
    wizard = enum.auto()
