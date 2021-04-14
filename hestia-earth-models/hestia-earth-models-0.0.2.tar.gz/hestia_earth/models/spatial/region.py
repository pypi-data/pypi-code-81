from hestia_earth.utils.api import download_hestia

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _linked_node
from .utils import download, has_geospatial_data


def _download_by_level(site: dict, level: int):
    field = f"GID_{level}"
    gadm_id = download(collection=f"users/hestiaplatform/gadm36_{level}",
                       ee_type='vector',
                       latitude=site.get('latitude'),
                       longitude=site.get('longitude'),
                       boundary=site.get('boundary'),
                       fields=field
                       ).get(field)
    try:
        return None if gadm_id is None else _linked_node(download_hestia(f"GADM-{gadm_id}"))
    except Exception:
        # the Term might not exist in our glossary if it was marked as duplicate
        return None


def _run(site: dict):
    for level in [5, 4, 3, 2, 1]:
        value = _download_by_level(site, level)
        if value is not None:
            logger.info('value=%s', value.get('@id'))
            break

    return value


def _should_run(site: dict):
    should_run = has_geospatial_data(site, by_region=False)
    logger.info('should_run=%s', should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else None
