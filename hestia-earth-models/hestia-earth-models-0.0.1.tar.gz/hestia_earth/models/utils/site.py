from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia, find_related


def _related_cycles(type: SchemaType, id: str):
    nodes = find_related(type, id, SchemaType.CYCLE)
    return [] if nodes is None else list(map(lambda node: download_hestia(node.get('@id'), SchemaType.CYCLE), nodes))
