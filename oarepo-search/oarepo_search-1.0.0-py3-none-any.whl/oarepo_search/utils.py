import json
from functools import lru_cache
from typing import List

from invenio_search import current_search


@lru_cache(maxsize=20)
def get_mapping(index_name) -> dict:
    mapping_path = current_search.mappings.get(index_name)
    with open(mapping_path, "r") as f:
        return json.load(f)


def replace_language_placeholder(field: str, languages: List[str]) -> List[str]:
    if "*" not in field:
        return [field]
    res = []
    for lang in languages:
        res.append(field.replace('*', lang))
    return res
