def compare_instances(x, y, instance_type) -> bool:
    return isinstance(x, instance_type) and isinstance(y, instance_type)


def list_diff(x: list, y: list, assert_only: bool = False) -> list:

    errors: list = []

    for idx, xv in enumerate(x):

        error_obj: dict = dict(x=xv)

        try:
            yv = y[idx]
        except IndexError:
            error_obj['type'] = 'MISSING'
            error_obj['field'] = '[{}]'.format(idx)
            error_obj['message'] = '[{}]: not found'.format(idx)
            errors.append(error_obj)
            continue

        if isinstance(xv, dict) and isinstance(yv, dict):
            sub_errors = json_diff(xv, yv)
            for error in sub_errors:
                error['field'] = '[{}].{}'.format(idx, error['field'])
                error['message'] = '[{}].{}'.format(idx, error['message'])
                errors.append(error)
            continue

        if xv != yv:
            error_obj['type'] = 'MISMATCH'
            error_obj['y'] = yv
            format_strings = dict(idx=idx, x=xv, type_x=type(xv).__name__, y=yv, type_y=type(yv).__name__)
            error_obj['message'] = '[{idx}]: {x} ({type_x}) != {y} ({type_y})'.format(**format_strings)
            errors.append(error_obj)

    if assert_only:
        return errors

    for idx, yv in enumerate(y):

        error_obj = {}

        if idx >= len(x):
            error_obj['y'] = yv
            error_obj['type'] = 'MISSING'
            error_obj['field'] = '[{}]'.format(idx)
            error_obj['message'] = '[{}]: not found'.format(idx)
            errors.append(error_obj)

    return errors


def compare_field(obj, field: str, value, ignore_missing_y_fields: bool) -> list:

    error = dict(field=field, x=value)

    if field not in obj:
        error['type'] = 'MISSING'
        error['message'] = '{}: not found'.format(field)
        return [error]

    if compare_instances(value, obj[field], dict):
        errors = json_diff(value, obj[field], ignore_missing_y_fields)
        for item in errors:
            item['field'] = '{}.{}'.format(field, item['field'])
            item['message'] = '{}.{}'.format(field, item['message'])
        return errors

    if compare_instances(value, obj[field], list):
        errors = list_diff(value, obj[field], ignore_missing_y_fields)
        for item in errors:
            item['field'] = '{}{}'.format(field, item['field']) if 'field' in item else field
            item['message'] = '{}{}'.format(field, item['message'])
        return errors

    if value != obj[field]:
        error['type'] = 'MISMATCH'
        error['y'] = obj[field]
        format_strings = dict(key=field, x=value, type_x=type(value).__name__,
                              y=obj[field], type_y=type(obj[field]).__name__)
        error['message'] = '{key}: {x} ({type_x}) != {y} ({type_y})'.format(**format_strings)
        return [error]

    return []


def json_diff(x: dict, y: dict, assert_only: bool = False) -> list:

    errors: list = []

    for k in x:
        errors += compare_field(y, k, x[k], assert_only)

    if assert_only:
        return errors

    for k in y:
        if k not in x:
            errors.append(dict(field=k, y=y[k], type='MISSING',
                               message='{}: not found'.format(k)))

    return errors


def compare(x, y, assert_only=False):

    if isinstance(x, dict) and isinstance(y, dict):
        return json_diff(x, y, assert_only=assert_only)

    if isinstance(x, list) and isinstance(y, list):
        return list_diff(x, y, assert_only=assert_only)
