from hestia_earth.models.log import logger

MODEL = 'primary'


def _find_primary_product(products: list):
    # If only one product, primary = True
    if len(products) == 1:
        return products[0]

    # else primary product = the product with the largest economic value share
    else:
        max_products = sorted(
            list(filter(lambda p: 'economicValueShare' in p.keys(), products)),  # take only products with value
            key=lambda k: k.get('economicValueShare'),  # sort by value
            reverse=True  # take the first as top value
        )
        if len(max_products) > 0:
            return max_products[0]

    return None


def _run(products: list):
    def run(product: dict):
        logger.info('model=%s, value=%s', MODEL, product.get('term', {}).get('@id'))
        product[MODEL] = True
        return product

    primary = _find_primary_product(products)
    return list(map(lambda p: run(p) if p == primary else p, products))


def _should_run(products: list):
    primary = next((p for p in products if p.get(MODEL, False) is True), None)
    should_run = len(products) > 0 and primary is None
    logger.info('model=%s, should_run=%s', MODEL, should_run)
    return should_run


def run(cycle: dict):
    products = cycle.get('products', [])
    return _run(products) if _should_run(products) else products
