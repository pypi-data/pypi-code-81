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


from tos.mixins.types import Mode
from tos.mixins.types import Proximity

from turberfield.catchphrase.drama import Drama


class Directing(Drama):
    """
    Leaving the game

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_quit)

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)

        if not self.player or not hasattr(self, "nav"):
            return rv

        locn = self.player.get_state(self.nav.Location)
        for obj in (i for i in self.ensemble if hasattr(i, "state") and i is not self.player):
            if obj.get_state(self.nav.Location) == locn:
                prox = obj.get_state(Proximity)
                if not prox or prox == Proximity.unknown:
                    obj.state = Proximity.present

        return rv

    def pause(self, quit=False):
        if quit:
            self.player.set_state(Mode.success)
            self.active.clear()
        else:
            self.player.set_state(Mode.pausing)

    def do_quit(self, this, text, /, **kwargs):
        """
        quit

        """
        self.pause(True)
        self.active.clear()
        yield ""
