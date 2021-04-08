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
import numbers
import operator

from turberfield.catchphrase.drama import Drama

from tos.mixins.types import Significance


class Telegraph(Drama):

    Messenger = namedtuple("Messenger", ["obj", "messages", "pending", "period"])

    def __init__(self, *args, messengers=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.messengers = messengers

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        for m in self.messengers[:]:
            if not m.obj.get_state(Significance):
                m.obj.state = Significance.notknown
            elif m.obj.get_state(Significance) == Significance.indicate:
                m.obj.state = Significance.emphasis
            elif m.obj.get_state(Significance) == Significance.suppress:
                continue

            if not m.messages:
                self.messengers.remove(m)
                continue

            p = m.pending
            if not p:
                state = m.obj.get_state(Significance)
                if isinstance(state, int):
                    m.obj.state = Significance.notknown

                if state in (Significance.notknown, Significance.inactive):
                    m.obj.state = Significance.indicate
                elif state == Significance.declined:
                    m.obj.state = Significance.inactive
                elif state == Significance.accepted:
                    m.obj.state = Significance.inactive
                    p = m.period
                    try:
                        m.messages.rotate(-1)
                    except AttributeError:
                        m.messages.pop(0)
            else:
                p -= 1

            self.messengers.remove(m)
            self.messengers.append(m._replace(pending=p))
        else:
            self.messengers.sort(key=operator.attrgetter("pending"))
        return rv
