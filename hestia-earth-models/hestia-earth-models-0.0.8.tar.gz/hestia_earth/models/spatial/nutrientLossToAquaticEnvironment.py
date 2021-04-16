from hestia_earth.schema import MeasurementStatsDefinition

from hestia_earth.models.log import logger
from hestia_earth.models.utils.measurement import _new_measurement
from .utils import download, has_geospatial_data, _site_gadm_id

TERM_ID = 'nutrientLossToAquaticEnvironment'
BIBLIO_TITLE = 'Modelling spatially explicit impacts from phosphorus emissions in agriculture'


def _measurement(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    measurement = _new_measurement(TERM_ID, BIBLIO_TITLE)
    measurement['value'] = [value]
    measurement['statsDefinition'] = MeasurementStatsDefinition.SPATIAL.value
    return measurement


def _run(site: dict):
    field = 'first'
    value = download(collection='users/hestiaplatform/r_fraction_loss_water',
                     ee_type='raster',
                     latitude=site.get('latitude'),
                     longitude=site.get('longitude'),
                     gadm_id=_site_gadm_id(site),
                     boundary=site.get('boundary'),
                     fields=field
                     ).get(field, None)

    return [] if value is None else [_measurement(value * 100)]


def _should_run(site: dict):
    should_run = has_geospatial_data(site)
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else []
