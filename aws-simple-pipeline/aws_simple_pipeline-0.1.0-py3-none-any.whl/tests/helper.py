import re
import yaml

def load(filename):
    return yaml.full_load(filename)

def remove_identifier(string):
    pattern = '[0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z]$'
    if re.match(pattern, string[-8:]):
        return re.sub(pattern, '', string)
    return string

def iterator(part_of_template):
    template = {}
    if isinstance(part_of_template, dict):
        for key in part_of_template.keys():
            new_key = remove_identifier(key)
            template[new_key] = iterator(part_of_template[key])
    if isinstance(part_of_template, list):
        values_list = []
        for value in part_of_template:
            values_list.append(iterator(value))
        template = values_list
    if isinstance(part_of_template, str):
        template = remove_identifier(part_of_template)
    return template

def remove_identifiers(original_template):
    template = {}
    for key in original_template.keys():
        template[key] = iterator(original_template[key])
    return template

def get_template(app, stack_name):
    template = app.synth().get_stack_by_name(stack_name).template
    return remove_identifiers(template)
