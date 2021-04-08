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
from collections import namedtuple
import random

from turberfield.catchphrase.drama import Drama
from turberfield.catchphrase.parser import CommandParser
from turberfield.dialogue.model import SceneScript


class Helpful(Drama):
    """
    Asking for help

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active.add(self.do_help)
        self.active.add(self.do_hint)
        self.active.add(self.do_history)

    def pause(self):
        pass

    def do_help(self, this, text, /, **kwargs):
        """
        help | ?

        """
        self.pause()
        active = {i.__name__: i for i in self.active}
        for c in reversed(self.__class__.__mro__):
            if c in (Drama, object):
                continue

            rv = []
            for a in dir(c):
                try:
                    fn = active.pop(a)
                    cmd, *others = random.choice(
                        [i for i in CommandParser.expand_commands(fn, self.ensemble) if len(i[0]) > 1]
                        # Filter out single letter commands for RST compatibility
                    )
                    rv.append("* {0}".format(cmd))
                except (IndexError, KeyError):
                    continue

            if rv and c.__doc__:
                yield "{0}:".format(c.__doc__.strip())

            yield "\n".join(rv)
        #yield "Start with a *look around*."
        #yield "To see a list of past actions, use the *history* command."
        #yield "Sometimes typing *hint* will give you an extra clue."

    def do_history(self, this, text, /, **kwargs):
        """
        history

        """
        self.pause()
        yield "[DRAMA]_"
        yield "So far, it's been like this."
        yield from ("*{0.args[0]}*".format(i) for i in reversed(self.history))

    def do_hint(self, this, text, /, **kwargs):
        """
        hint

        """
        yield ""
