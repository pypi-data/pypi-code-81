import fsspec
import geopandas
import pathlib
import pystac
import pytest
import tempfile
import xarray as xr

from stac2dcache.utils import catalog2geopandas, copy_asset, get_asset

from . import test_data_path


@pytest.fixture(scope='function')
def catalog():
    catalog_path = test_data_path / "s2-catalog"
    return pystac.Catalog.from_file(
            (catalog_path/"catalog.json").as_posix()
        )


@pytest.fixture(scope='function')
def catalog_with_assets():
    catalog_dir = "test-catalog"
    with tempfile.TemporaryDirectory() as tmpdir:
        catalog_path = test_data_path / catalog_dir
        catalog = pystac.Catalog.from_file(
            (catalog_path/"catalog.json").as_posix()
        )
        tmp_catalog_path = pathlib.Path(tmpdir) / catalog_dir
        catalog.normalize_and_save(
            tmp_catalog_path.as_posix(),
            "SELF_CONTAINED"
        )
        yield catalog


def test_catalog2geopandas_returns_correct_data_type(catalog):
    gdf = catalog2geopandas(catalog)
    assert isinstance(gdf, geopandas.GeoDataFrame)


def test_catalog2geopandas_returns_correct_indices(catalog):
    gdf = catalog2geopandas(catalog)
    item_ids = [i.id for i in catalog.get_all_items()]
    assert gdf.index.size == len(item_ids)
    assert all([i in gdf.index for i in item_ids])


def test_catalog2geopandas_returns_all_catalog_fields(catalog):
    gdf = catalog2geopandas(catalog)
    item = next(catalog.get_all_items())
    assert all([i in gdf.columns for i in item.properties.keys()])


def test_catalog2geopandas_returns_correct_crs(catalog):
    gdf = catalog2geopandas(catalog)
    assert gdf.crs == "WGS84"


def test_catalog2geopandas_returns_correct_crs_with_custom_value(catalog):
    # assume the input catalog uses a different CRS - not actually true
    custom_crs = "EPSG:3031"
    gdf = catalog2geopandas(catalog, crs=custom_crs)
    assert gdf.crs == custom_crs


def test_copy_asset_for_all_items(catalog_with_assets):
    copy_asset(catalog_with_assets, asset_key="tile")
    for item in catalog_with_assets.get_all_items():
        item_path = pathlib.Path(item.get_self_href())
        item_dir = item_path.parent
        for asset in item.assets.values():
            asset_path = pathlib.Path(asset.get_absolute_href())
            # assets should be in the dir folders
            assert asset_path.name in [el.name for el in item_dir.iterdir()]
            # assets href should have not been updated
            assert item_dir.as_posix() not in asset_path.as_posix()


def test_copy_asset_for_a_single_item(catalog_with_assets):
    item_id = "tile_1"
    copy_asset(catalog_with_assets, asset_key="tile", item_id=item_id)
    for item in catalog_with_assets.get_all_items():
        item_path = pathlib.Path(item.get_self_href())
        item_dir = item_path.parent
        for asset in item.assets.values():
            asset_path = pathlib.Path(asset.get_absolute_href())
            dir_elements = [el.name for el in item_dir.iterdir()]
            # assets should be in the dir folders
            if item.id == item_id:
                assert asset_path.name in dir_elements
            else:
                assert asset_path.name not in dir_elements


def test_copy_asset_updates_catalog(catalog_with_assets):
    copy_asset(catalog_with_assets, asset_key="tile", update_catalog=True)
    for item in catalog_with_assets.get_all_items():
        item_path = pathlib.Path(item.get_self_href())
        item_dir = item_path.parent
        for asset in item.assets.values():
            asset_path = pathlib.Path(asset.get_absolute_href())
            # assets should be in the dir folders
            assert asset_path.name in [el.name for el in item_dir.iterdir()]
            # assets href should have been updated
            assert item_dir.as_posix() in asset_path.as_posix()


def test_copy_asset_to_custom_path(catalog_with_assets):
    with tempfile.TemporaryDirectory() as tmpdir:
        copy_asset(catalog_with_assets, asset_key="tile", to_uri=tmpdir)
        tmpdir_path = pathlib.Path(tmpdir)
        for item in catalog_with_assets.get_all_items():
            elements = [el.name for el in (tmpdir_path/item.id).iterdir()]
            for asset in item.assets.values():
                asset_path = pathlib.Path(asset.get_absolute_href())
                # assets should be in the tmp dir
                assert asset_path.name in elements
                # assets href should have not been updated
                assert tmpdir_path.as_posix() not in asset_path.as_posix()


def test_get_asset_returns_correct_data_type(catalog_with_assets):
    asset = get_asset(catalog_with_assets, asset_key="tile", item_id="tile_1")
    assert isinstance(asset, xr.DataArray)


def test_get_asset_works_with_custom_filesystem(catalog_with_assets):
    fs = fsspec.get_filesystem_class("file")
    fs = fs()
    asset = get_asset(catalog_with_assets, asset_key="tile", item_id="tile_1",
                      filesystem=fs)
    assert isinstance(asset, xr.DataArray)


def test_get_asset_works_with_custom_drivers(catalog_with_assets):
    asset = get_asset(catalog_with_assets, asset_key="tile", item_id="tile_1",
                      driver="rasterio")
    assert isinstance(asset, xr.DataArray)
    asset = get_asset(catalog_with_assets, asset_key="tile", item_id="tile_1",
                      driver="raw")
    assert isinstance(asset, bytes)
