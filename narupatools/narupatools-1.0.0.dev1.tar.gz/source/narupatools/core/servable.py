# This file is part of narupatools (https://gitlab.com/alexjbinnie/narupatools).
# Copyright (c) University of Bristol. All rights reserved.
#
# narupatools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# narupatools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with narupatools.  If not, see <http://www.gnu.org/licenses/>.

"""
Abstract base class for objects which need to perform actions when added or removed from a NarupaSession.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod

import narupatools.core.session as session


class Servable(metaclass=ABCMeta):
    """
    Abstract base class for object that can be broadcast on a Narupa Session and requires callbacks for when it
    is added and removed.
    """

    @abstractmethod
    def start_being_served(self, server: session.NarupaSession) -> None:
        """Called when this object is shown by a Narupa session."""
        ...

    @abstractmethod
    def end_being_served(self, server: session.NarupaSession) -> None:
        """Called when this object is stopped being shown by a Narupa session."""
        ...
