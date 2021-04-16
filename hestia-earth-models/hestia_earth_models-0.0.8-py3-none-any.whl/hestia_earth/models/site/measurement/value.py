from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _average
from hestia_earth.models.utils.measurement import _new_measurement


def _run(measurement: dict):
    value = _average(measurement.get('min') + measurement.get('max'))
    logger.info('term=%s, value=%s', measurement.get('term', {}).get('@id'), value)
    measurement = _new_measurement(measurement.get('term'))
    measurement['value'] = [value]
    return measurement


def _should_run(measurement: dict):
    return ('value' not in measurement or len(measurement['value']) == 0) and \
        len(measurement.get('min', [])) > 0 and len(measurement.get('max', [])) > 0


def run(site: dict):
    measurements = list(filter(_should_run, site.get('measurements', [])))
    return non_empty_list(map(_run, measurements))
