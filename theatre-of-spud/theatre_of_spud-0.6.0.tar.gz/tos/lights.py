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

import enum
import random

from turberfield.dialogue.types import EnumFactory

from tos.mixins.carrying import Carrying
from tos.mixins.moving import Moving
from tos.mixins.types import Artifact
from tos.mixins.types import Awareness
from tos.mixins.types import Proximity
from tos.mixins.types import Significance

from tos.map import Map

@enum.unique
class Switch(EnumFactory, enum.Enum):
    broken = 0
    closed = 1
    opened = 2


class Lights(Carrying, Moving):
    """Operating lights"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self, ensemble=None):
        ensemble = ensemble or []
        n = next((n for n, i in enumerate(ensemble) if "fuse" in i.names), None)
        yield ensemble.pop[n] if n is not None else Artifact(
            names=["fuse"],
            detail={
                0: ["It's an inline fuse.", "It says, '13A'."],
                Proximity.carried: ["It's an inline fuse.", "It says, '13A'."]
            },
        ).set_state(Awareness.ignorant)

        n = next((n for n, i in enumerate(ensemble) if "lights" in i.names), None)
        yield ensemble.pop[n] if n is not None else Artifact(
            names=["lights"],
            detail={
                Significance.indicate: ["On the wall is a chunky metal switch."],
                Awareness.discover: [
                    "It's a switch for the lights outside.",
                    "This switch operates the lights in the Car park."
                ],
                Awareness.familiar: [
                    "There's an empty slot here.",
                    "The little neon lamp is out."
                ],
                Switch.closed: ["The switch is in the 'on' position."],
                Switch.opened: ["The switch is in the 'off' position."],
            },
        ).set_state(Awareness.ignorant, Switch.opened)

        yield from super().build(ensemble)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        fuse = next(iter(self.lookup["fuse"]))
        lights = next(iter(self.lookup["lights"]))
        for obj in (fuse, lights):
            if self.player.get_state(self.nav.Location) == obj.get_state(self.nav.Location):
                if obj is fuse:
                    self.active.add(self.do_get)
                else:
                    self.active.discard(self.do_get)
                if obj.get_state(Significance) == Significance.indicate:
                    self.active.add(self.do_lights_off)
                    self.active.add(self.do_lights_on)
                    obj.state = Awareness.discover

        if fuse.get_state(self.nav.Location) == lights.get_state(self.nav.Location):
            self.active.add(self.do_fit_fuse)
        else:
            self.active.discard(self.do_fit_fuse)
        return rv

    def do_go(self, this, text, /, *args, locn: Map.Location):
        """
        enter {locn.value[0]}
        enter {locn.value[1]}
        enter {locn.value[2]}
        go {locn.value[0]} | go to {locn.value[0]}
        go {locn.value[1]} | go to {locn.value[1]}
        go {locn.value[2]} | go to {locn.value[2]}

        """
        yield from super().do_go(this, text, locn=locn)

    def do_fit_fuse(self, this, text, *args):
        """
        fit fuse
        fit fuse in light
        put fuse in slot

        """
        next(iter(self.lookup["fuse"])).state = Awareness.complete
        next(iter(self.lookup["lights"])).state = Awareness.complete
        yield ""

    def do_lights_off(self, this, text, *args):
        """
        switch off lights | switch lights off
        turn off lights | turn lights off

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = Awareness.familiar
        if lights.get_state(Switch) == Switch.opened:
            yield "The switch is already in the 'off' position."
        else:
            lights.state = Switch.opened
            if lights.get_state(Awareness) == Awareness.complete:
                yield "The exterior lights go out."
            else:
                yield random.choice([
                    "The switch goes to the 'off' position.",
                    "The switch clicks off.",
                ])

    def do_lights_on(self, this, text, *args):
        """
        switch on lights | switch lights on
        turn on lights | turn lights on

        """
        lights = next(iter(self.lookup["lights"]))
        lights.state = Awareness.familiar
        if lights.get_state(Switch) == Switch.closed:
            yield "The switch is already in the 'on' position."
        else:
            lights.state = Switch.closed
            if lights.get_state(Awareness) == Awareness.complete:
                yield random.choice([
                    "The exterior lights come on.",
                ])
            else:
                yield random.choice([
                    "The switch goes to the 'on' position.",
                    "The switch clicks on.",
                ])
                yield random.choice([
                    "But the lights aren't working.",
                    "Nothing happens outside.",
                ])

        lights.state = Switch.closed
        if lights.get_state(Awareness) == Awareness.complete:
            yield "The exterior lights come on."
