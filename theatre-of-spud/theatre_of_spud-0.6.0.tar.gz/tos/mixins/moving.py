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

from collections import defaultdict
from collections import deque
import enum
import functools
import random

from turberfield.dialogue.model import SceneScript

from tos.mixins.navigator import Navigator
from tos.mixins.directing import Directing
from tos.mixins.types import Motion
from tos.mixins.types import Proximity


class Moving(Directing):
    "Physical space"

    def __init__(self, nav: Navigator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nav = nav
        self.active.add(self.do_go)
        self.active.add(self.do_look)
        self.active.add(self.do_next)
        self.active.add(self.do_where)

    @property
    def location(self):
        locn = self.player.get_state(self.nav.Location)
        return random.choice(self.nav.spots[locn.name])

    @property
    def scenery(self):
        locn = self.player.get_state(self.nav.Location)
        return random.choice(self.nav.scenery[locn.name])

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)

        mobs = [self.player] + [i for i in self.ensemble if hasattr(i, "state") and i is not self.player]
        for mob in mobs:
            if not mob.get_state(self.nav.Location):
                continue
            if (mob.get_state(self.nav.Arriving)
                and mob.get_state(self.nav.Arriving).name != mob.get_state(self.nav.Location).name
            ):
                route = list(self.nav.route(
                    mob.get_state(self.nav.Location), mob.get_state(self.nav.Arriving)
                ))
                route.pop(0)
                if route:
                    mob.state = Motion.routed
                    mob.state = route.pop(0)

                if not route:
                    mob.state = Motion.static

            if not self.player.get_state(self.nav.Location):
                continue
            elif mob.get_state(Proximity) == Proximity.carried:
                mob.state = self.player.get_state(self.nav.Location)
                continue

            hops = list(self.nav.route(
                mob.get_state(self.nav.Location), self.player.get_state(self.nav.Location)
            ))
            prox = Proximity.outside
            if (mob.get_state(self.nav.Departed)
                and mob.get_state(self.nav.Departed).name == self.player.get_state(self.nav.Location).name
            ):
                prox = Proximity.outward
            elif (mob.get_state(self.nav.Arriving)
                and mob.get_state(self.nav.Arriving).name == self.player.get_state(self.nav.Location).name
            ):
                prox = Proximity.inbound

            mob.state = {
                0: Proximity.unknown,
                1: Proximity.present,
                2: prox,
            }.get(len(hops), Proximity.distant)
        return rv

    def do_go(self, this, text, /, *args, locn: Navigator.__subclasses__()):
        """
        enter {locn.value[0]}
        enter {locn.value[1]}
        enter {locn.value[2]}
        go {locn.value[0]} | go to {locn.value[0]}
        go {locn.value[1]} | go to {locn.value[1]}
        go {locn.value[2]} | go to {locn.value[2]}

        """
        self.player.state = self.player.get_state(self.nav.Location)
        self.player.state = self.nav.Departed[self.player.get_state(self.nav.Location).name]
        self.player.state = self.nav.Arriving[locn.name]
        hops = list(self.nav.route(
            self.player.get_state(self.nav.Location), self.player.get_state(self.nav.Arriving)
        ))
        if len(hops) > 2:
            yield f"{self.player.name} heads off to the {locn.value[0]}."
        else:
            yield f"{self.player.name} moves towards the {locn.value[0]}."

    def do_look(self, this, text, *args):
        """
        look | look around

        """
        locn = self.player.get_state(self.nav.Location)
        yield "**{0}**".format(locn.value[0].title())
        yield random.choice(["Exits are:", "We are close to:", "Nearby:"])
        yield from (
            "* the {0}".format(self.nav.Location[i].value[0].title()) for i in self.nav.topology[locn.name]
        )

    def do_next(self, this, text, *args):
        """
        n | next

        """
        yield f"{self.player.name} is {self.scenery}."

    def do_where(self, this, text, *args):
        """
        w | wait
        where | where am i | where is it

        """
        yield f"{self.player.name} is {self.scenery}."
