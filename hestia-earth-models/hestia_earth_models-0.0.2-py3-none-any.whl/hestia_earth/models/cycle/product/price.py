
from hestia_earth.utils.lookup import get_table_value, column_name, download_lookup
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.lookup import _extract_grouped_data

MODEL = 'price'


def _product(product: dict, value: float):
    # divide by 1000 to convert price per tonne to kg
    value = value / 1000
    logger.info('model=%s, value=%s, term=%s', MODEL, value, product.get('term', {}).get('@id'))
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

    return product if value is None else _product(product, value)


def _should_run(product: dict):
    should_run = MODEL not in product.keys() and len(product.get('value', [])) > 0
    logger.info('model=%s, should_run=%s, term=%s', MODEL, should_run, product.get('term', {}).get('@id'))
    return should_run


def run(cycle: dict):
    return list(map(lambda p: _run(cycle, p) if _should_run(p) else p, cycle.get('products', [])))
