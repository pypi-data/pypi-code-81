from hestia_earth.models.log import logger
from hestia_earth.models.utils import _average


def _should_run_measurement(measurement: dict):
    return ('value' not in measurement or len(measurement['value']) == 0) and \
        len(measurement.get('min', [])) > 0 and len(measurement.get('max', [])) > 0


def _measurement(measurement: dict):
    value = _average(measurement.get('min') + measurement.get('max'))
    logger.info('term=%s, value=%s', measurement.get('term', {}).get('@id'), value)
    measurement['value'] = [value]
    return measurement


def _should_run(site: dict):
    measurements = list(filter(_should_run_measurement, site.get('measurements', [])))
    should_run = len(measurements) > 0
    logger.info('gap_fill=%s', should_run)
    return should_run, measurements


def run(site: dict):
    should_run, measurements = _should_run(site)
    return list(map(_measurement, measurements)) if should_run else []
