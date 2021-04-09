import urlpath

from .rasterio import RasterioDriver
from .raw import RawDriver
from .textfiles import TextfilesDriver


drivers = {
    'rasterio': RasterioDriver,
    'raw': RawDriver,
    'textfiles': TextfilesDriver,
}


suffix2driver = {
    '.tif': 'rasterio',
    '.jp2': 'rasterio',
    '.xml': 'textfiles',
}


def get_driver(uri, driver=None):
    """
    Find and initialize driver for an asset

    :param uri: (string) URI to the asset
    :param driver: (optional, string) name of the required driver
    """
    suffix = urlpath.URL(uri).suffix
    driver = driver or suffix2driver.get(suffix)
    if driver is None:
        raise ValueError(f'Unknown driver for suffix: {suffix}')
    driver = drivers.get(driver)
    if driver is None:
        raise ValueError(f'Unknown driver: {driver}')
    return driver(uri)
