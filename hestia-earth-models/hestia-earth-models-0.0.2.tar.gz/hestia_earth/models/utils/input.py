from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia

from . import _linked_node, _term_id


def _new_input(term):
    input = {'@type': SchemaType.INPUT.value}
    input['term'] = _linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return input
