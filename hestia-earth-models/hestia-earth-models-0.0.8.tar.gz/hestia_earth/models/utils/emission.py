from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia

from . import _term_id, _linked_node


def _new_emission(term):
    node = {'@type': SchemaType.EMISSION.value}
    node['term'] = _linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return node
