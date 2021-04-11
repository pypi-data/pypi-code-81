from wtforms import (
    Form,
    FormField,
    BooleanField,
    DecimalField,
    FloatField,
    IntegerField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    validators
)

FIELD_TYPES = [
    'string',
    'integer',
    'decimal',
    'float',
    'select',
    'select_multiple',
    'radio',
    'boolean'
]

FORM_FIELD_MAP = {
    'string': lambda label, f: StringField(l, get_field_validators(f))
}

filters = [lambda x: x or '']

def get_field_validators(field_info):
    validator_list = []
    field_validators = field_info.get('validators', {})
    # Set Reqired
    if field_validators.get('required', False):
        validator_list.append(validators.InputRequired())
    # String Min/Max Length
    if field_info.get('type') == 'input':
        length_kwargs = {}
        min_length = field_validators.get('min_length', None)
        if min_length:
            length_kwargs['min'] = min_length
        max_length = field_validators.get('max_length', None)
        if max_length:
            length_kwargs['max'] = max_length
        if len(length_kwargs):
            validator_list.append(validators.Length(**length_kwargs))
    # Float/Integer Validators
    if field_info.get('type') in ['float', 'integer']:
        length_kwargs = {}
        min_length = field_validators.get('min', None)
        if min_length:
            length_kwargs['min'] = min_length
        max_length = field_validators.get('max', None)
        if max_length:
            length_kwargs['max'] = max_length
        if len(length_kwargs):
            validator_list.append(validators.NumberRange(**length_kwargs))
    # Return Validators
    return validator_list

def get_field_class(field_info):
    validator_list = []
    label = field_info.get('label')
    validator_list = get_field_validators(field_info)
    field_type = field_info.get('type')
    if field_type == 'string':
        return StringField(label, validator_list, filters)
    elif field_type == 'integer':
        return IntegerField(label, validator_list, filters)
    elif field_type == 'decimal':
        return DecimalField(label, validator_list, filters)
    elif field_type == 'float':
        return FloatField(label, validator_list, filters)
    elif field_type == 'select':
        return SelectField(label, choices=field_info.get('choices', []), filters=filters)
    elif field_type == 'select_multiple':
        return SelectMultipleField(label, choices=field_info.get('choices', []), filters=filters)
    elif field_type == 'radio':
        return RadioField(label, choices=field_info.get('choices', []), filters=filters)
    elif field_type == 'boolean':
        return BooleanField(label, default=field_info.get('default', False), filters=filters)
    raise Exception(
        f'Field Type "{field_type}" is not a supported '+
        f'field type. Supported field types are: {", ".join(FIELD_TYPES)}.'
    )

def create_wtform_from_schema(schema):
    """class NexusForm(Form): pass"""
    NF = type('NexusForm', (Form,), {})
    for field_name, field_info in schema.items():
        field_class = get_field_class(field_info)
        if field_class:
            setattr(NF, field_name, field_class)
    return NF
