from typing import Callable, Any


def clean(obj: Any, reject: Callable[[str, Any], bool]) -> Any:
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(obj, list):
        return clean_list(obj, reject)
    elif isinstance(obj, dict):
        return clean_dict(obj, reject)
    else:
        return obj


def clean_dict(dict_to_clean: dict, reject: Callable[[str, Any], bool]) -> dict:
    cleaned_dict = {key: clean(value, reject) for key, value in dict_to_clean.items() if not reject(key, value)}
    return cleaned_dict


def clean_list(list_to_clean: list, reject: Callable[[str, Any], bool]) -> list:
    cleaned_list = [clean(list_item, reject) for list_item in list_to_clean if not reject(None, list_item)]
    return cleaned_list
