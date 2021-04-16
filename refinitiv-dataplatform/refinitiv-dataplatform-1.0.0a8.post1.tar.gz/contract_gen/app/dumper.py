import logging
import os
import textwrap
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from app.parsers import parse_inheritance
from app.types import simple_types, INSTRUMENT_DEFINITION, INSTRUMENT_PRICING_PARAMS, DEFINITION
from app.utils import camel_to_snake, get_first_word
from config_gen import Config

logger = logging.getLogger(__name__)

env = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader('./app/templates'),
)
env.globals.update(camel_to_snake=camel_to_snake)
env.globals.update(indent=textwrap.indent)
env.globals.update(now=datetime.utcnow)

class_definition_template = env.get_template('class_definition.py.j2')
class_instrument_template = env.get_template('class_instrument.py.j2')
class_pricing_params_template = env.get_template('class_pricing_params.py.j2')
enum_template = env.get_template('enum.py.j2')
init_template = env.get_template('__init__.py.j2')


def priority_getter(name):
    priority = Config.PRIORITY_BY_ARG_NAME.get(name)
    return priority if priority else Config.PRIORITY_BY_ARG_NAME['__default__']


def date_priority_getter(name):
    priority = Config.PRIORITY_BY_DATE.get(name)
    return priority if priority else Config.PRIORITY_BY_DATE['__default__']


def dump(stream, root_path, module_name, file_name):
    path = os.path.join(root_path, module_name, f'{file_name}.py')
    dir_path = os.path.join(root_path, module_name)

    if os.path.exists(dir_path):
        stream.dump(path)

    else:
        logger.warning(f'{path} does not exists. It will be created.')
        os.makedirs(dir_path)
        stream.dump(path)


def dump_enums(enums_by_hash):
    dumped_count = 0
    import_enums = []
    for enum_hash, enum in enums_by_hash.items():
        enum_name = enum.get('name')
        enum_value = enum.get('value')
        enum_value = sorted(enum_value, key=date_priority_getter, reverse=True)
        import_enums.append(camel_to_snake(enum_name))
        stream = enum_template.stream(
            class_name=enum_name,
            items=enum_value
        )
        stream.dump(os.path.join(Config.ENUM_DUMP_PATH, f'{camel_to_snake(enum_name)}.py'))
        dumped_count += 1

    #
    stream = init_template.stream(
        import_names=import_enums
    )
    stream.dump(os.path.join(Config.ENUM_DUMP_PATH, '__init__.py'))
    logger.info(f'Dumped {dumped_count} enums.')


def get_key_by_value(d, value):
    for k, v in d.items():
        if value in v:
            return k


def get_filename(fn):
    return os.path.splitext(fn)[0]


def dump_classes(class_by_name, class_by_module_name, enum_by_hash):
    dumped_count = 0
    models_class_names = []
    for class_name, props in class_by_name.items():
        complex_props = props.get('complex_props')
        simple_props = props.get('simple_props')
        module_name = props.get('module_name')

        if complex_props:
            for item in complex_props:
                *head, prop_type, _ = item

                if prop_type == 'enum':
                    _, enum_hash = head
                    enum = enum_by_hash[enum_hash]
                    item[1] = enum.get('name')

        if class_name in Config.DO_NOT_DUMP:
            continue

        props_names = [n for n, *_ in complex_props] + [n for n, *_ in simple_props]
        props_names = sorted(props_names, key=priority_getter, reverse=True)
        inheritance = parse_inheritance(class_name)

        if len(class_by_module_name[module_name]) == 1:
            # print(module_name, class_name, inheritance)
            pass

        if inheritance == INSTRUMENT_DEFINITION:
            import_enums = set([
                class_n
                for _, class_n, type_n, *_ in complex_props
                if type_n == 'enum'
            ])
            import_models = set([
                class_n
                for _, class_n, type_n, *_ in complex_props
                if type_n not in simple_types and type_n != 'enum'
            ])
            stream = class_instrument_template.stream(
                class_name=get_first_word(class_name),
                props_names=props_names,
                simple_props=simple_props,
                complex_props=complex_props,
                import_enums=[{'file_name': camel_to_snake(item), 'class_name': item} for item in import_enums],
                import_models=[{'file_path': camel_to_snake(item), 'class_name': item} for item in import_models]
            )
            module_path = props.get('module_path', Config.IPA_ROOT_DUMP_PATH)
            if module_path != Config.IPA_ROOT_DUMP_PATH:
                module_name = ""
            dump(stream, root_path=module_path, module_name=module_name, file_name=f"_{camel_to_snake(class_name)}")
            dumped_count += 1

        elif inheritance == INSTRUMENT_PRICING_PARAMS:
            import_enums = set([
                class_n
                for _, class_n, type_n, *_ in complex_props
                if type_n == 'enum'
            ])
            import_models = set([
                class_n
                for _, class_n, type_n, *_ in complex_props
                if type_n not in simple_types and type_n != 'enum'
            ])
            stream = class_pricing_params_template.stream(
                class_name=class_name,
                props_names=props_names,
                simple_props=simple_props,
                complex_props=complex_props,
                import_enums=[{'file_name': camel_to_snake(item), 'class_name': item} for item in import_enums],
                import_models=[
                    {'file_path': camel_to_snake(get_key_by_value(class_by_module_name, item)), 'class_name': item}
                    for item
                    in import_models
                ]
            )
            module_path = props.get('module_path', Config.IPA_ROOT_DUMP_PATH)
            if module_path != Config.IPA_ROOT_DUMP_PATH:
                module_name = ""
            dump(stream, root_path=module_path, module_name=module_name, file_name=f"_{camel_to_snake(class_name)}")
            dumped_count += 1

        elif inheritance == DEFINITION:  # models
            models_class_names.append(camel_to_snake(class_name))
            import_enums = set([
                class_n
                for _, class_n, type_n, *_ in complex_props
                if type_n == 'enum'
            ])
            import_models = set([
                class_n
                for _, class_n, type_n, *_ in complex_props
                if type_n not in simple_types and type_n != 'enum'
            ])
            stream = class_definition_template.stream(
                class_name=class_name,
                props_names=props_names,
                simple_props=simple_props,
                complex_props=complex_props,
                import_enums=[{'file_name': camel_to_snake(item), 'class_name': item} for item in import_enums],
                import_models=[
                    {'file_path': camel_to_snake(get_key_by_value(class_by_module_name, item)), 'class_name': item}
                    for item
                    in import_models
                ]
            )
            module_path = props.get('module_path', Config.MODELS_DUMP_PATH)
            if class_name in Config.MODELS:
                defined_module_name = camel_to_snake(class_name)
            else:
                defined_module_name = props.get('defined_module_name', f"_{camel_to_snake(class_name)}")
            dump(stream, root_path=module_path, module_name="", file_name=defined_module_name)
            dumped_count += 1

        else:
            raise Exception(class_name)

    models_filenames = [get_filename(fn) for fn in os.listdir(Config.MODELS_DUMP_PATH) if fn not in ['__init__.py', '__pycache__']]
    #
    stream = init_template.stream(
        import_names=models_filenames,
        delete_refs=models_filenames
    )
    stream.dump(os.path.join(Config.MODELS_DUMP_PATH, '__init__.py'))
    logger.info(f'Dumped {dumped_count} classes.')
