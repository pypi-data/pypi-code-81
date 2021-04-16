from hestia_earth.utils.model import find_primary_product, find_term_match
from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.property import _get_property_value
from hestia_earth.models.utils.cycle import _is_term_type_incomplete
from hestia_earth.models.utils.product import _new_product
from .residue.residueRemoved import TERM_ID as PRACTICE_TERM_ID
from .aboveGroundCropResidueRemoved import TERM_ID as REMOVED_TERM_ID

TERM_ID = 'aboveGroundCropResidueTotal'
PROPERTY_KEY = 'dryMatter'


def _get_removed_practice_value(cycle: dict) -> float:
    value = find_term_match(cycle.get('practices', []), PRACTICE_TERM_ID).get('value')
    return safe_parse_float(value) / 100 if value is not None else None


def _get_value(primary_product: dict, dm_percent: float):
    lookup = download_lookup('crop.csv', True)

    term_id = primary_product.get('term', {}).get('@id', '')
    product_yield = primary_product.get('value', [0])[0]

    in_lookup = term_id in list(lookup.termid)
    logger.debug('Found lookup data for Term: %s? %s', term_id, in_lookup)

    if in_lookup:
        # Multiply yield by dryMatter proportion
        yield_dm = product_yield * (dm_percent / 100)

        # estimate the AG DM calculation
        ag_slope = safe_parse_float(
            get_table_value(lookup, 'termid', term_id, 'crop_residue_slope'), None
        )
        ag_intercept = safe_parse_float(
            get_table_value(lookup, 'termid', term_id, 'crop_residue_intercept'), None
        )
        logger.debug('term=%s, yield=%s, dry_matter_percent=%s, slope=%s, intercept=%s',
                     term_id, product_yield, dm_percent, ag_slope, ag_intercept)

        # estimate abv. gro. residue as dry_yield * slope + intercept * 1000.  IPCC 2006 (Poore & Nemecek 2018)
        return None if ag_slope is None or ag_intercept is None else (yield_dm * ag_slope + ag_intercept * 1000)

    return None


def _product(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    product = _new_product(TERM_ID)
    product['value'] = [value]
    return product


def _run(cycle: dict, primary_product: dict, removed_value: float, dm_property: dict):
    practice_value = _get_removed_practice_value(cycle)

    value = _get_value(primary_product, safe_parse_float(dm_property.get('value'))) \
        if removed_value is None or practice_value is None else removed_value / practice_value

    return [_product(value)] if value is not None else []


def _get_removed_value(cycle: dict):
    # if we find the removed value, we can infer the total
    value = find_term_match(cycle.get('products', []), REMOVED_TERM_ID, {'value': []}).get('value')
    return value[0] if len(value) > 0 else None


def _should_run(cycle: dict):
    product = find_primary_product(cycle)
    dm_property = _get_property_value(product, PROPERTY_KEY) if product is not None else None
    removed_value = _get_removed_value(cycle)
    should_run = (removed_value is not None or dm_property is not None) \
        and _is_term_type_incomplete(cycle, TERM_ID)
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run, product, removed_value, dm_property


def run(cycle: dict):
    should_run, product, removed_value, dm_property = _should_run(cycle)
    return _run(cycle, product, removed_value, dm_property) if should_run else []
