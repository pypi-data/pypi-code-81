from typing import get_type_hints

from dataclasses_json import dataclass_json
from docstring_parser import parse

from grebble_flow.managment.processor import find_all_processors


def get_processors_info():
    result = []
    processors = find_all_processors()
    for processor in processors:
        item = {"name": processor.name}
        docs = parse(processor.attributes.__doc__)
        if hasattr(processor, "attributes"):
            item['attributes_schema'] = get_type_hints(processor.attributes)
            for key in item['attributes_schema']:
                docsItem = [x for x in docs.params if x.arg_name == key]
                item['attributes_schema'][key] = {
                    "type": item['attributes_schema'][key].__name__,
                    "description": docsItem[0].description if docsItem else ""
                }
        result.append(item)
    return result


def generate_package_info():
    result = {"processors": get_processors_info()}
    return result
