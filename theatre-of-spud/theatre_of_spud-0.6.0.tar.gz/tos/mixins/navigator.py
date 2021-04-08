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


from turberfield.dialogue.types import EnumFactory


class Navigator(EnumFactory):

    routes = {}

    def route(self, locn, dest):
        if (locn.name, dest.name) in self.routes:
            return self.routes[(locn.name, dest.name)]

        typ = type(locn)
        rvs = set()
        paths = [[locn]]
        n = len(self.topology)
        d = 1
        while n >= 0 or not rvs:
            nxt = []
            for p in paths:
                if p[-1].name == dest.name:
                    rvs.add(tuple(p))
                else:
                    nodes = self.topology[p[-1].name]
                    d = len(nodes)
                    for i in nodes:
                        nxt.append(p.copy())
                        nxt[-1].append(typ[i])
            paths = nxt
            n = n - d

        rv = sorted(rvs, key=len)[0] if rvs else []
        self.routes[(locn.name, dest.name)] = rv
        return rv
