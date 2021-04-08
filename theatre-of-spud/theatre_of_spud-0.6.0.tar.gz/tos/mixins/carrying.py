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
from tos.mixins.navigator import Navigator
from tos.mixins.types import Artifact
from tos.mixins.types import Awareness
from tos.mixins.types import Proximity
from tos.mixins.types import Mode


class Carrying(Moving):
    """Handling objects"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_get)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        if self.player.get_state(Mode) == Mode.success:
            return rv

        if any(
            i for i in self.ensemble
            if isinstance(i, Artifact)
            and self.player.get_state(self.nav.Location) == i.get_state(self.nav.Location)
        ):
            self.active.add(self.do_get)
        else:
            self.active.discard(self.do_get)

        mobs = [
            i for i in self.ensemble
            if hasattr(i, "state") and i.get_state(Proximity) == Proximity.carried
        ]
        if mobs:
            self.active.add(self.do_examine)

        for mob in mobs:
            mob.state = self.player.get_state(self.nav.Location)
        return rv

    def interpret(self, options):
        locn = self.player.get_state(self.nav.Location)
        text = ""
        for fn, args, kwargs in options:
            text = args[0]
            if all(
                isinstance(i, Navigator)
                or i.get_state(self.nav.Location) == locn
                or i.get_state(Proximity) == Proximity.carried
                for i in kwargs.values()
            ):
                return (fn, args, kwargs)
        else:
            return (None, [text], {})

    def do_get(self, this, text, /, *, obj: Artifact):
        """
        get {obj.names[0]}
        pick up {obj.names[0]}

        """
        locn = self.player.get_state(self.nav.Location)
        if obj.get_state(self.nav.Location) != locn:
            yield f"There is no {obj.name} here."
            return

        obj.state = self.nav.Departed[locn.name]
        obj.state = Proximity.carried
        yield f"Now carrying the {obj.name}."

    def do_look(self, this, text, *args):
        """
        look | look around

        """
        yield from super().do_look(this, text, *args)
        carrying = {
            i for i in self.ensemble
            if isinstance(i, Artifact) and i.get_state(Proximity) == Proximity.carried
        }
        artifacts = [
            i for i in self.ensemble
            if isinstance(i, Artifact) and i not in carrying
            and self.player.get_state(self.nav.Location) == i.get_state(self.nav.Location)
        ]
        if carrying:
            yield "Carrying:"
            yield from ("* {0.names[0]}".format(i) for i in carrying)
        if artifacts:
            yield random.choice(["In view:", "We can see:"])
            yield from ("* {0.names[0]}".format(i) for i in artifacts)

    def do_examine(self, this, text, /, *args, obj: Artifact):
        """
        check {obj.names[0]}
        examine {obj.names[0]}

        """
        state = obj.get_state(Proximity)
        yield random.choice(obj.detail.get(state, [""]))
