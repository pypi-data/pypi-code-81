from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import logger
from hestia_earth.models.utils.cycle import _is_term_type_complete
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidue.aboveGroundCropResidueBurnt import TERM_ID as PRODUCT

TERM_ID = 'nh3ToAirCropResidueBurning'
DRY_MATTER_FACTOR_TO_NH3 = 2.17/1000


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    return emission


def _run(product_value: list):
    value = sum(product_value)
    return [_emission(value * DRY_MATTER_FACTOR_TO_NH3)]


def _get_product_value(cycle: dict):
    product_value = find_term_match(cycle.get('products', []), PRODUCT, {}).get('value', [])
    return [0] if len(product_value) == 0 and _is_term_type_complete(cycle, PRODUCT) else product_value


def _should_run(cycle: dict):
    product_value = _get_product_value(cycle)
    should_run = len(product_value) > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, product_value


def run(cycle: dict):
    should_run, product_value = _should_run(cycle)
    return _run(product_value) if should_run else []
