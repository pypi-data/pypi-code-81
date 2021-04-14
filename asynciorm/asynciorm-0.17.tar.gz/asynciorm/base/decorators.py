from ..exceptions import ValidateError


def pre_validate_fields(func):
    async def wrapper(*args, **params):
        fields = args[0].model._fields
        for param in params:
            if fields.get(param if not param.endswith('_id') else param.replace('_id', '')) is None:
                raise ValidateError(f'Unknown field - {param}')

        return await func(*args, **params)

    return wrapper

