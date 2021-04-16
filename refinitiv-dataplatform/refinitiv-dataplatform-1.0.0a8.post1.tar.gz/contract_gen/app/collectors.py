import os

from app.errors import UnsolvableCollision, CantFindCommonName
from app.types import py_types_by_simple_types, py_types_by_complex_types
from app.utils import camel_case_split, remove_unicode_symbols, camel_to_snake
from config_gen import Config

import logging

logger = logging.getLogger(__name__)

enum_by_hash = {}
enum_by_name = {}


def get_hash_by_value(list_str):
    list_str.sort()
    return "".join(s for s in list_str)


def collect_enum(input_name, input_value):
    input_name = Config.ENUM_ALIASES.get(input_name, input_name)
    input_hash = get_hash_by_value(input_value)
    exist_enum = enum_by_hash.get(input_hash)

    if exist_enum:
        exists_name = exist_enum.get('name')

        if exists_name != input_name:
            splitted_exists_name = camel_case_split(exists_name, lower=True)
            splitted_input_name = camel_case_split(input_name, lower=True)
            common = [n for n in splitted_exists_name if n in splitted_input_name]

            if not common:
                raise CantFindCommonName(exists_name, input_name, input_value)

            name = "".join(n.title() for n in common)

        else:
            name = exists_name

    else:
        name = f'{input_name[0].upper()}{input_name[1:]}'

    exist_enum = enum_by_name.get(name)

    if exist_enum:
        exist_hash = exist_enum.get('hash')

        if exist_hash != input_hash:
            raise UnsolvableCollision(name, input_hash, exist_hash)

    enum = {'name': name, 'value': input_value, 'hash': input_hash}
    enum_by_hash[input_hash] = enum
    enum_by_name[name] = enum


classes_by_name = {}
classes_by_inheritance = {}
classes_by_module_name = {}


def collect_class(class_name, data):
    from app.parsers import parse_inheritance

    simple_props = []
    complex_props = []

    for k, v in data.get('properties').items():
        desc = v.get('description')
        desc = remove_unicode_symbols(desc)
        prop_type = v.get('type')
        ref = v.get('$ref')
        enum_value = v.get('enum')

        if not prop_type and ref:
            *_, items_type = ref.rsplit('/', 1)
            items_type = Config.RENAME_CLASS.get(items_type, items_type)
            complex_props.append([k, items_type, 'object', desc])

        elif prop_type and prop_type == 'array':
            items = v.get('items')
            ref = items.get('$ref')
            items_type = items.get('type')

            if not items_type and not ref:
                raise Exception(prop_type, items)

            if ref:
                *_, items_type = ref.rsplit('/', 1)
            items_type = Config.RENAME_CLASS.get(items_type, items_type)
            complex_props.append([k, items_type, py_types_by_complex_types[prop_type], desc])

        elif prop_type and enum_value:
            complex_props.append([k, get_hash_by_value(enum_value), 'enum', desc])

        elif not prop_type and not ref:
            raise Exception(k)

        elif py_types_by_simple_types.get(prop_type):
            simple_props.append([k, py_types_by_simple_types[prop_type], desc])

        else:
            logger.warning(f"[Warning] Can't collect {k}:{prop_type} property, not enough data.")

    simple_props.sort()
    complex_props.sort()

    exists_class = classes_by_name.get(class_name)
    if exists_class:
        exists_simple_props = exists_class.get('simple_props')
        exists_complex_props = exists_class.get('complex_props')

        if exists_simple_props != simple_props:
            raise Exception(class_name, exists_simple_props, simple_props)

        if exists_complex_props != complex_props:
            raise Exception(class_name, exists_complex_props, complex_props)

    else:

        #
        class_props = {}

        first, *_ = camel_case_split(class_name)
        module_name = first.lower()

        if class_name in Config.MODULE_PATH_BY_CLASS_NAME.keys():
            module_path = Config.MODULE_PATH_BY_CLASS_NAME.get(class_name)
            class_props['module_path'] = os.path.join(Config.IPA_ROOT_DUMP_PATH, module_path)

        if class_name in Config.MODELS:
            module_name = ".models"

        class_name = Config.RENAME_CLASS.get(class_name, class_name)

        classes_names = classes_by_module_name.setdefault(module_name, [])
        classes_names.append(class_name)

        class_props['class_name'] = class_name
        class_props['module_name'] = module_name
        class_props['simple_props'] = simple_props
        class_props['complex_props'] = complex_props

        #
        classes_by_name[class_name] = class_props

        #
        inheritors = classes_by_inheritance.setdefault(parse_inheritance(class_name), [])
        inheritors.append(classes_by_name[class_name])
