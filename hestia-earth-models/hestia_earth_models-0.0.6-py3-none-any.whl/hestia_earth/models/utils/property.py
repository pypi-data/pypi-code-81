from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match

from . import _term_id, _linked_node


def _new_property(term):
    node = {'@type': SchemaType.PROPERTY.value}
    node['term'] = _linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return node


def _find_term_property(term_id: str, property: str):
    term = download_hestia(term_id)
    return find_term_match(term.get('defaultProperties', []), property, None)


def _get_property_value(value: dict, property: str):
    prop = find_term_match(value.get('properties', []), property, None)
    return _find_term_property(value.get('term', {}).get('@id'), property) if prop is None else prop
