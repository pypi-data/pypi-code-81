from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.product import _new_product

MODEL = 'economicValueShare'


def _product(term: dict, value: float):
    logger.info('model=%s, value=%s, term=%s', MODEL, value, term.get('@id'))
    product = _new_product(term)
    product[MODEL] = value
    return product


def _should_run_p(product: dict):
    should_run = MODEL not in product.keys()
    logger.info('model=%s, should_run=%s, term=%s', MODEL, should_run, product.get('term', {}).get('@id'))
    return should_run


def _run(product: dict):
    lookup = download_lookup('crop.csv', True)

    # If revenue available for all products (or above 50% for any product), econValueShare = revenue/sum
    # (revenue all products in the cycle)*100
    # TODO: add this calculation

    # If no revenue provided = use country level averages for the given product (for example, wheat 80%; straw 20%)
    term = product.get('term', {}).get('@id', '')
    # TODO: need to ensure that when combining uploaded data on EVS with calculated EVS, the sum not > 100.
    value = safe_parse_float(get_table_value(lookup, 'termid', term, 'global_economic_value_share'), None)
    return None if value is None else _product(product.get('term', {}), value)


def _should_run(products: list):
    total_value = sum([p.get(MODEL, 0) for p in products])
    return total_value < 100


def run(cycle: dict):
    products = cycle.get('products', [])
    should_run = _should_run(products)
    products = list(filter(_should_run_p, products)) if should_run else []
    return non_empty_list(map(_run, products))
