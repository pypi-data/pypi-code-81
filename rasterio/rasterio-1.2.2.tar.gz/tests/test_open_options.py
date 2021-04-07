"""Tests of dataset opening options and driver choice"""

import pytest

import rasterio
from rasterio.transform import Affine

from .conftest import requires_only_gdal1, requires_gdal2, requires_gdal22


@requires_gdal2
def test_fail_with_missing_driver():
    """Fail to open a GeoTIFF without the GTiff driver"""
    with pytest.raises(rasterio.errors.RasterioIOError):
        rasterio.open('tests/data/RGB.byte.tif', driver='BMP')


@requires_gdal2
def test_open_specific_driver():
    """Open a GeoTIFF with the GTiff driver"""
    with rasterio.open('tests/data/RGB.byte.tif', driver='GTiff') as src:
        assert src.count == 3


@requires_gdal22
def test_open_specific_driver_with_options():
    """Open a GeoTIFF with the GTiff driver and GEOREF_SOURCES option"""
    with rasterio.open(
            'tests/data/RGB.byte.tif', driver='GTiff', GEOREF_SOURCES='NONE') as src:
        assert src.transform == Affine.identity()
