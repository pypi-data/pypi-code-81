from app.collectors import collect_class, collect_enum
from app.errors import UnsolvableCollision
from app.types import simple_types, complex_types, DEFINITION, INSTRUMENT_PRICING_PARAMS, INSTRUMENT_DEFINITION
from app.utils import get_first_word
from config_gen import Config
import logging

logger = logging.getLogger(__name__)


def get_by_ref(data, ref, key=''):
    if ref is None:
        return key, {}

    if ref == "":
        return key, data

    key, *lref = ref.split('/', 1)
    ref = "".join(lref)

    if key != "#":
        data = data.get(key)

    return get_by_ref(data, ref, key)


def parse_inheritance(class_name):
    inheritance_name = Config.DEFINE_INHERITANCE_EXPLICIT.get(class_name)

    if inheritance_name == 'DEFINITION':
        return DEFINITION

    inheritance = DEFINITION

    if class_name in Config.INHERITANCE_INSTRUMENT_DEFINITION:
        inheritance = INSTRUMENT_DEFINITION

    elif class_name.endswith('PricingParameters'):
        inheritance = INSTRUMENT_PRICING_PARAMS

    return inheritance


def parse_type(value, key, parsed_keys, root):
    parsed_type = value.get('type')
    ref = value.get('$ref')

    if parsed_type and ref:
        raise Exception(key)

    if not parsed_type and not ref:
        raise Exception(key)

    data = None
    if parsed_type is None and ref:
        parsed_keys.append('$ref')
        key, data = get_by_ref(root, ref)
        parsed_type = data.get('type')

        if parsed_type == 'object':
            parsed_type = key

    elif parsed_type:
        parsed_keys.append('type')

    return parsed_type, data


def parse_items(prop_key, items_value, root):
    items_type, items_data = parse_type(items_value, prop_key, [], root)

    if items_type == 'array':
        items_type, items_data = parse_items(prop_key, items_value.get('items'), root)

    if items_type not in simple_types and not items_data:
        raise Exception(prop_key, items_type, items_value)

    if items_type not in simple_types:
        collect_class(items_type, items_data)

    return items_type, items_data


def parse_properties(owner, owner_type, value, root, class_tree, indent, _items_type=None):
    if not value:
        return

    properties = value.get('properties', {})
    for prop_key, prop_value in properties.items():
        parsed_keys = []

        desc = prop_value.get('description')
        if desc:
            parsed_keys.append('description')

        prop_type, data = parse_type(prop_value, prop_key, parsed_keys, root)
        data_type = data and data.get('type') or prop_type

        if data_type == 'object' and prop_type == 'object' and not data:
            logger.warning(f"[Warning] In {_items_type} class, property {prop_key} without data")
            continue

        if data_type == 'object':
            collect_class(prop_type, data)
            class_tree.append("{} {}:{}\t(object)".format('\t' * indent, prop_key, prop_type))
        else:
            class_tree.append("{} {}:{}".format('\t' * indent, prop_key, prop_type))

        if data_type not in simple_types and data_type not in complex_types:
            raise Exception(prop_type, data_type)

        enum_value = prop_value.get('enum')
        format_value = prop_value.get('format')
        items_value = prop_value.get('items')
        read_only_value = prop_value.get('readOnly', None)
        example_value = prop_value.get('example', None)

        if read_only_value is not None:
            parsed_keys.append('readOnly')
            logger.warning("[Warning] 'readOnly' value parsed, but not saved to class_tree")

        if example_value is not None:
            parsed_keys.append('example')
            logger.warning("[Warning] 'example' value parsed, but not saved to class_tree")

        if enum_value:

            try:
                collect_enum(prop_key, enum_value)
            except UnsolvableCollision as e:
                enum_name = get_first_word(owner_type) + e.name
                logger.info(f'{e.name} -> {enum_name}')
                collect_enum(enum_name, enum_value)

            parsed_keys.append('enum')
            class_tree[-1] += f":enum"
            class_tree.append("{} {}\t(enum)".format('\t' * (indent + 1), enum_value))

        if format_value:
            parsed_keys.append('format')
            class_tree.append("{} {}\t(format)".format('\t' * (indent + 1), format_value))

        if items_value:
            parsed_keys.append('items')
            items_type, items_data = parse_items(prop_key, items_value, root)
            class_tree[-1] += f":{items_type}\t(items)"
            parse_properties(prop_key, prop_type, items_data, root, class_tree, indent + 1, items_type)

        keys_list = list(prop_value.keys())

        if sorted(keys_list) != sorted(parsed_keys):
            raise Exception(f'{prop_key} has {keys_list} fields, but parsed only {parsed_keys}.')

        parse_properties(prop_key, prop_type, data, root, class_tree, indent + 1)


def parse_json(root):
    class_tree = []
    count = 0

    definitions = root.get('definitions')
    for key, value in definitions.items():

        if key in Config.INCLUDE:
            count += 1
            collect_class(key, value)
            class_tree.append(f'{count}.{key}')
            parse_properties(key, "", value, root, class_tree, 1)

    return class_tree
