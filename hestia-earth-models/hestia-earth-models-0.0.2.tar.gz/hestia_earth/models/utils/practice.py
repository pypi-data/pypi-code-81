from hestia_earth.schema import PracticeJSONLD
from hestia_earth.utils.api import download_hestia

from . import _term_id, _linked_node


def _new_practice(term):
    node = PracticeJSONLD().to_dict()
    node['term'] = _linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return node
