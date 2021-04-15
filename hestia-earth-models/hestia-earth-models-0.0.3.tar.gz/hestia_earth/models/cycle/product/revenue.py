from hestia_earth.models.log import logger

MODEL = 'revenue'


def _run(product: dict):
    value = product.get('value', [1])[0] * product.get('price', 0)
    logger.info('model=%s, value=%s, term=%s', MODEL, value, product.get('term', {}).get('@id'))
    product[MODEL] = value
    return product


def _should_run(product: dict):
    should_run = MODEL not in product.keys() and len(product.get('value', [])) > 0 and product.get('price', 0) > 0
    logger.info('model=%s, should_run=%s, term=%s', MODEL, should_run, product.get('term', {}).get('@id'))
    return should_run


def run(cycle: dict):
    return list(map(lambda p: _run(p) if _should_run(p) else p, cycle.get('products', [])))
