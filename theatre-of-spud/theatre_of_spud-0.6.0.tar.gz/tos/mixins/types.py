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

from collections import defaultdict
from collections import deque
import enum
import random

from turberfield.dialogue.types import DataObject
from turberfield.dialogue.types import EnumFactory
from turberfield.dialogue.types import Stateful


class Named(DataObject):

    @property
    def name(self):
        return random.choice(getattr(self, "names", [""]))


class Material(Stateful):

    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent or self

    def get_state(self, typ=int, default=0):
        """Report state from parent. """
        if self.parent is self:
            return super().get_state(typ, default)
        else:
            return self.parent.get_state(typ, default)


class Space(Named, Stateful):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contents(self, ensemble):
        return [i for i in ensemble if getattr(i, "parent", None) is self]


class Artifact(Named, Stateful): pass
class Character(Named, Stateful): pass

class Awareness(EnumFactory, enum.Enum):

    ignorant = enum.auto()
    rumoured = enum.auto()
    discover = enum.auto()
    familiar = enum.auto()
    complete = enum.auto()
    remember = enum.auto()


class Significance(EnumFactory, enum.Enum):

    notknown = enum.auto()
    inactive = enum.auto()
    indicate = enum.auto()
    emphasis = enum.auto()
    elevated = enum.auto()
    alarming = enum.auto()
    suppress = enum.auto()
    accepted = enum.auto()
    declined = enum.auto()
    reducing = enum.auto()
    diminish = enum.auto()
    silenced = enum.auto()
    resolved = enum.auto()


class Proximity(EnumFactory, enum.Enum):

    audible = enum.auto()
    carried = enum.auto()
    distant = enum.auto()
    huddled = enum.auto()
    inbound = enum.auto()
    outside = enum.auto()
    outward = enum.auto()
    present = enum.auto()
    tactile = enum.auto()
    unknown = enum.auto()
    visible = enum.auto()
    whisper = enum.auto()


class Mode(EnumFactory, enum.Enum):

    default = enum.auto()
    develop = enum.auto()
    monitor = enum.auto()
    pausing = enum.auto()
    playing = enum.auto()
    preplay = enum.auto()
    success = enum.auto()
    testing = enum.auto()
    visitor = enum.auto()
    warning = enum.auto()


class Motion(EnumFactory, enum.Enum):

    broken = enum.auto()
    follow = enum.auto()
    leader = enum.auto()
    moving = enum.auto()
    patrol = enum.auto()
    routed = enum.auto()
    static = enum.auto()
    sticky = enum.auto()
