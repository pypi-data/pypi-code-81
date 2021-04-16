from hestia_earth.utils.tools import non_empty_list
from hestia_earth.models.log import logger
from hestia_earth.models.utils.product import _new_product

MODEL = 'revenue'


def _run(product: dict):
    value = product.get('value', [1])[0] * product.get('price', 0)
    logger.info('model=%s, value=%s, term=%s', MODEL, value, product.get('term', {}).get('@id'))
    product = _new_product(product.get('term', {}))
    product[MODEL] = value
    return product


def _should_run(product: dict):
    should_run = MODEL not in product.keys() and len(product.get('value', [])) > 0 and product.get('price', 0) > 0
    logger.info('model=%s, should_run=%s, term=%s', MODEL, should_run, product.get('term', {}).get('@id'))
    return should_run


def run(cycle: dict):
    products = list(filter(_should_run, cycle.get('products', [])))
    return non_empty_list(map(_run, products))
