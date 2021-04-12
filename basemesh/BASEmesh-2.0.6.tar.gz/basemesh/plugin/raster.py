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

"""Helper method for supporting rasterized elevation sources."""

import math
from qgis.core import QgsPointXY, QgsRasterLayer  # type: ignore
from ..abc import ElevationSource
from ..types import Point2D


class RasterDataWrapper(ElevationSource):
    """Wrapper class for QgsRasterLayer.

    This class allows usage of QgsRasterLayer as an interpolation
    source.
    """

    def __init__(self, layer: QgsRasterLayer, band_id: int = 0) -> None:
        """Instantiate the raster data wrapper.

        Note that this function uses a 0-based band index. The actual
        interpolation function uses a 1-based index, but this is
        converted internally.
        Be sure to pass the regular band index into this initialiser,
        i.e. the same you would use to retrieve the band name by index.

        Parameters
        ----------
        layer : QgsRasterLayer
            The raster layer to wrap
        band_id : int, optional
            The 0-based band index, by default 0
        """
        self.layer = layer
        self.band = band_id
        self.provider = layer.dataProvider()

    def elevation_at(self, point: Point2D) -> float:
        """Return the elevation at the given point.

        Parameters
        ----------
        point : Tuple[float, float]
            The point to interpolate

        Returns
        -------
        float
            The elevation of the data source at the given point

        Raises
        ------
        ValueError
            Raised if the data source could not provide a value for the
            given sample point
        """
        # Query the data provider for the elevation at the given point
        point_xy = QgsPointXY(*point)

        # NOTE: Important:
        # Although it is not currently marked as such in the documentation, the
        # QgsRasterDataProvider.sample() method is available to the Python
        # API.
        # Its arguments seem to be mostly the same, but the ok parameter has
        # been replaced with a second return value instead.
        #
        # Also, for reasons unknown, it uses band indices starting at 1.
        value, is_valid = self.provider.sample(point_xy, self.band+1)

        # If no match could be found, raise a ValueError
        if not is_valid or math.isnan(value):
            raise ValueError(f'Unable to interpolate point {point}')

        return float(value)
