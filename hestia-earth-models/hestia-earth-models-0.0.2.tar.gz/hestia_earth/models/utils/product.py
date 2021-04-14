from hestia_earth.schema import ProductJSONLD
from hestia_earth.utils.api import download_hestia

from . import _linked_node, _term_id


def _new_product(term):
    product = ProductJSONLD().to_dict()
    product['term'] = _linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return product
