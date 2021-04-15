import functools
from typing import Dict, Any, List


def list_delete_empty_items(list_arg: list) -> list:
    """Delete items from the list_arg is the item is an empty strings, empty list, zero, False or None."""
    empty_values = ('', [], 0, False, None)
    # TODO: not sure if this is the right way to implement this
    return [i for i in list_arg if i not in empty_values]


def copy_first_arg_dict(func):
    """If the first arg is a dictionary, pass a copy of the dictionary into func."""
    import copy

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_dict = args[0]
        other_args = args[1:]

        if isinstance(first_arg_dict, dict):
            first_arg_dict_copy = copy.deepcopy(first_arg_dict)
            return func(first_arg_dict_copy, *other_args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


@copy_first_arg_dict
def dict_add(dictionary: Dict[Any, List[Any]], key: Any, value: Any) -> Dict[Any, List[Any]]:
    """Add the given value to the dictionary at the given key. This function expects that all values of the dictionary parameter are lists."""
    if key in dictionary:
        if not isinstance(dictionary[key], list):
            message = f'The value at the "{key}" key in the dictionary is not a list and the dict_add function requires all values to be a list.'
            raise TypeError(message)
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]
    return dictionary
