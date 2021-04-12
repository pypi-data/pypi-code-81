# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Processing algorithms contributed by BASEmesh."""

import os
from typing import Any
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider  # type: ignore
from ..utils import get_plugin_dir
from . import converters, matid

__all__ = [
    'BasemeshProcessingProvider'
]


class BasemeshProcessingProvider(QgsProcessingProvider):
    """Processing algorithm provider for BASEmesh."""

    def loadAlgorithms(self) -> None:
        """Load all algorithms provided by the provider."""
        self.addAlgorithm(converters.LegacyLineTo3DLine())
        self.addAlgorithm(converters.LegacyPointTo3DPoint())
        self.addAlgorithm(matid.AssignMaterialID())
        self.addAlgorithm(matid.ExtractMaterialID())

    @staticmethod
    def id() -> str:
        """Return the unique processing provider ID."""
        return 'basemesh'

    @staticmethod
    def name() -> str:
        """Return the user-friendly name of the processing provider."""
        return 'BASEmesh'

    @staticmethod
    def icon() -> Any:
        """Return the QIcon to use for the processing provider."""
        return QIcon(os.path.join(
            get_plugin_dir(), 'plugin', 'icons', 'basemesh_icon.svg'))
