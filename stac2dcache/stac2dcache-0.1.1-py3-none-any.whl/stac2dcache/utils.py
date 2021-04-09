import geopandas
import urlpath

from concurrent.futures import ProcessPoolExecutor, as_completed

from .drivers import get_driver
from .io import IO


def catalog2geopandas(catalog, crs=None):
    """
    Create a geopandas data-frame with the catalog items

    :param catalog: (:class:`~pystac.Catalog`) input catalog
    :param crs: (string or accepted CRS object) coordinate reference system
        employed in the catalog (default is WGS84)
    :return: :class:`~geopandas.GeoDataFrame`
    """
    crs = crs or "WGS84"
    features = {item.id: item.to_dict() for item in catalog.get_all_items()}
    gdf = geopandas.GeoDataFrame.from_features(features.values())
    gdf.index = features.keys()
    gdf = gdf.set_crs(crs)
    return gdf


def copy_asset(catalog, asset_key, update_catalog=False, item_id=None,
               to_uri=None, filesystem_from=None, filesystem_to=None,
               max_workers=None):
    """
    Download an asset for (one of) the items of a catalog

    :param catalog: (:class:`~pystac.Catalog`) input catalog
    :param asset_key: (str) asset key
    :param update_catalog: (bool) update the catalog links to the new asset
        location (default: False)
    :param item_id: (optional, str) item ID (default: retrieve assets for all
        items of the catalog)
    :param to_uri: (optional, str) URI of the folder where to save the assets
        (default: the catalog's item directories)
    :param filesystem_from: (optional, `fsspec` compatible FileSystem instance)
        file system for input source
    :param filesystem_to: (optional, `fsspec` compatible FileSystem instance)
        file system for output destination
    :param max_workers: (optional, int) number of processes that will be used
        to copy the assets (default to number of processors)
    """
    io = IO(filesystem_from=filesystem_from, filesystem_to=filesystem_to)

    root_href = catalog.get_self_href()
    if root_href is None and to_uri is None:
        raise ValueError('Provide URI where to save the assets '
                         '(or save the catalog to disk)')

    if item_id is not None:
        item = catalog.get_item(item_id, recursive=True)
        if item is not None:
            items = (item,)
        else:
            raise ValueError(f'Item not found: {item_id}')
    else:
        items = catalog.get_all_items()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:

        future_to_asset = {}
        for item in items:
            asset = item.assets.get(asset_key)
            if asset is None:
                raise ValueError(f'Asset {asset_key} not found for {item.id}')
            if to_uri is not None:
                destination = urlpath.URL(to_uri) / item.id
            else:
                destination = urlpath.URL(item.get_self_href()).parent
            future = executor.submit(
                io.copy,
                from_uri=asset.get_absolute_href(),
                to_uri=destination,
            )
            future_to_asset[future] = asset

        for future in as_completed(future_to_asset):
            new_href = future.result()
            if update_catalog:
                asset = future_to_asset[future]
                asset.href = new_href  # update link in catalog


def get_asset(catalog, asset_key, item_id, driver=None, filesystem=None,
              **kwargs):
    """
    Get an asset from the catalog using one of the available drivers

    :param catalog: (:class:`~pystac.Catalog`) input catalog
    :param asset_key: (str) asset key
    :param item_id: (str) item ID
    :param driver: (optional, str) name of the driver to read the asset
        (default: guess the driver from the asset's extension)
    :param filesystem: (optional, `fsspec` compatible FileSystem instance)
        file system of input source
    :param kwargs: (optional) keyword arguments passed on to the driver, e.g.
                   `chunks` for raster data or `blocksize` for text files.
    :return: asset read
    """
    item = catalog.get_item(item_id, recursive=True)
    asset = item.assets.get(asset_key)
    driver = get_driver(uri=asset.get_absolute_href(), driver=driver)
    driver.set_filesystem(filesystem)
    return driver.get(**kwargs)
