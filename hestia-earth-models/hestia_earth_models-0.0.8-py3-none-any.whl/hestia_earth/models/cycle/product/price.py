
from hestia_earth.utils.lookup import get_table_value, column_name, download_lookup
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.lookup import _extract_grouped_data
from hestia_earth.models.utils.product import _new_product

MODEL = 'price'


def _product(term: dict, value: float):
    # divide by 1000 to convert price per tonne to kg
    value = value / 1000
    logger.info('model=%s, value=%s, term=%s', MODEL, value, term.get('@id'))
    product = _new_product(term)
    product[MODEL] = value
    return product


def _run(cycle: dict, product: dict):
    crop_lookup = download_lookup('crop.csv', True)

    # TODO: add description saying this is based on annual value averaged between 1991-2018, source: FAOSTAT
    lookup = download_lookup('region-crop-cropGroupingPrice.csv')

    country_id = cycle.get('site').get('country').get('@id')
    term_id = product.get('term', {}).get('@id', '')
    grouping = get_table_value(crop_lookup, 'termid', term_id, column_name('cropGroupingPrice'))
    price_data = get_table_value(lookup, 'termid', country_id, column_name(grouping)) if grouping else None
    avg_price = _extract_grouped_data(price_data, 'Average_price_per_tonne')
    value = safe_parse_float(avg_price, None)
    return None if value is None else _product(product.get('term', {}), value)


def _should_run(product: dict):
    should_run = MODEL not in product.keys() and len(product.get('value', [])) > 0
    logger.info('model=%s, should_run=%s, term=%s', MODEL, should_run, product.get('term', {}).get('@id'))
    return should_run


def run(cycle: dict):
    products = list(filter(_should_run, cycle.get('products', [])))
    return non_empty_list(map(lambda p: _run(cycle, p), products))
