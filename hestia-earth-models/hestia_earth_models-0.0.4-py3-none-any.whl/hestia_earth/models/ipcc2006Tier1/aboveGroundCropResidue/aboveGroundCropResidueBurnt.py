from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from .aboveGroundCropResidueRemoved import TERM_ID as REMOVED_TERM_ID

TERM_ID = 'aboveGroundCropResidueBurnt'


def _get_value(term_id: str, total_product: float, removed_product: float, practice_value: float):
    lookup = download_lookup('crop.csv', True)

    in_lookup = term_id in list(lookup.termid)
    logger.debug('Found lookup data for Term: %s? %s', term_id, in_lookup)

    if in_lookup:
        # 1) Calculate amount burnt in kg (accounting for amount removed)
        burnt_kg = (total_product - removed_product) * practice_value

        # 2) Gap-fill amount burnt in kg by multiplying by the combustion factor
        comb_factor = safe_parse_float(
            get_table_value(lookup, 'termid', term_id, 'combustion_factor_crop_residue')
        )
        # These are global combustion factors - from IPCC 2006
        return None if comb_factor is None else burnt_kg * comb_factor

    return None


def should_run(cycle: dict, primary_product: dict = None):
    return primary_product is not None


def _find_removed_product(cycle: dict, added_products: list):
    # removed might come from original or added data
    products = cycle.get('products', []) + added_products
    return find_term_match(products, REMOVED_TERM_ID)


def run(cycle: dict, primary_product: dict, total_value: float, practice_value: float, products: list = []):
    removed_product = _find_removed_product(cycle, products)
    removed_value = safe_parse_float(removed_product.get('value', [0])[0], 0)
    term_id = primary_product.get('term', {}).get('@id', '')
    return _get_value(term_id, total_value, removed_value, practice_value)
