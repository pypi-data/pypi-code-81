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

import random

from tos.mixins.moving import Moving
from tos.mixins.telegraph import Telegraph
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact
from tos.mixins.types import Significance


class Calls(Telegraph, Moving):
    """Taking phone calls"""

    def __call__(self, fn, *args, **kwargs):
        yield from super().__call__(fn, *args, **kwargs)

        for m in self.messengers:
            if m.obj.get_state(Significance) == Significance.indicate:
                yield random.choice([
                    "Suddenly, the {0.obj.name} rings.".format(m),
                    "The {0.obj.name} starts to ring.".format(m),
                    "The {0.obj.name} begins ringing.".format(m),
                ])
            elif m.obj.get_state(Significance) in (
                Significance.emphasis, Significance.elevated, Significance.alarming
            ):
                yield random.choice([
                    "The {0.obj.name} rings again.".format(m),
                    "The {0.obj.name} continues to ring.".format(m),
                    "The {0.obj.name} is still ringing.".format(m),
                ])

    def build(self, ensemble=None):
        yield from super().build(ensemble)
        yield Artifact(
            names=["phone", "telephone"],
            detail={},
            messages=[],
        ).set_state(Awareness.ignorant)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        self.active.discard(self.do_receive_call)
        for m in self.messengers:
            if m.obj.get_state(Significance) not in (
                Significance.notknown, Significance.inactive, Significance.silenced,
                Significance.suppress, Significance.resolved
            ):
                m.obj.state += 1
                if self.player.get_state(self.nav.Location) == m.obj.get_state(self.nav.Location):
                    self.active.add(self.do_receive_call)
        return rv

    def do_receive_call(self, this, text, /, *args, obj: Artifact):
        """
        answer {obj.names[0]} | answer the {obj.names[0]}
        get {obj.names[0]} | get the {obj.names[0]}
        pick up {obj.names[0]} | pick up the {obj.names[0]}

        """
        obj.state = 0
        obj.state = Significance.suppress
        yield f"{self.player.name} answers the {obj.name}"

