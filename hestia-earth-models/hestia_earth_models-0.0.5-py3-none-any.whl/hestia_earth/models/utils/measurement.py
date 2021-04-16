from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia, find_node_exact

from . import _average, _linked_node, _term_id


def _new_measurement(term, biblio_title=None):
    node = {'@type': SchemaType.MEASUREMENT.value}
    node['term'] = _linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    if biblio_title:
        source = find_node_exact(SchemaType.SOURCE, {'bibliography.title': biblio_title})
        if source:
            node['source'] = _linked_node({'@type': SchemaType.SOURCE.value, **source})
    return node


def measurement_value_average(measurement: dict): return _average(measurement.get('value', [0]))
