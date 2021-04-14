from hestia_earth.utils.model import find_primary_product

from hestia_earth.models.log import logger


def _run(impact: dict):
    primary_product = find_primary_product(impact.get('cycle', {})).get('term')
    logger.info('value=%s', primary_product.get('@id'))
    return primary_product


def _should_run(impact: dict):
    should_run = find_primary_product(impact.get('cycle', {})) is not None
    logger.info('should_run=%s', should_run)
    return should_run


def run(impact: dict): return _run(impact) if _should_run(impact) else None
