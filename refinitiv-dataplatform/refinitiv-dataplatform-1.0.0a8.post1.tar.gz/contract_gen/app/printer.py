from jinja2 import Environment, FileSystemLoader

from app.dumper import priority_getter
from app.utils import camel_to_snake
import random

env = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader('./app/templates'),
)
env.globals.update(camel_to_snake=camel_to_snake)

ctor_desc = env.get_template('ctor_desc.j2')
test_parameter = env.get_template('test_parameter.j2')
functions_template = env.get_template('functions.j2')


def print_functions(contract_name):
    print(functions_template.render(contract_name=contract_name))


def print_classes_to_file(class_by_name, class_by_module_name, enum_by_hash):
    ctor_desc_string, test_parameter_string = print_classes(class_by_name, class_by_module_name, enum_by_hash)
    with open('ctor_desc.txt', 'w') as f:
        f.write(ctor_desc_string)
    with open('test_parameter.txt', 'w') as f:
        f.write(test_parameter_string)


def print_classes(class_by_name, class_by_module_name, enum_by_hash):
    ctor_desc_string = ""
    test_parameter_string = ""
    for class_name, props in class_by_name.items():
        complex_props = props.get('complex_props')

        if complex_props:
            for item in complex_props:
                *head, prop_type, _ = item

                if prop_type == 'enum':
                    _, enum_hash = head
                    enum = enum_by_hash[enum_hash]
                    item[1] = enum.get('name')

        simple_props = props.get('simple_props')
        module_name = props.get('module_name')
        class_props = [(p_name, p_type, p_desc) for p_name, p_type, _, p_desc in complex_props] + simple_props
        class_props = sorted(class_props, key=lambda x: priority_getter(x[0]), reverse=True)
        ctor_desc_string += ctor_desc.render(
            class_props=class_props,
            file_name=f"_{camel_to_snake(class_name)}"
        )
        test_parameter_string += test_parameter.render(
            class_props=class_props,
            file_name=f"_{camel_to_snake(class_name)}"
        )
    return ctor_desc_string, test_parameter_string


def print_enums(enum_by_hash):
    template = "({}, {}.{}),"
    for enum_hash, v in enum_by_hash.items():
        enum_name = v.get('name')
        rand_enum_item = camel_to_snake(random.choice(v.get('value')), upper=True)
        print(template.format(enum_name, enum_name, rand_enum_item))
