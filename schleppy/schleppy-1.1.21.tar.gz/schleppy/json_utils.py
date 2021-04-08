import re
from collections import OrderedDict


def convert_dict(source, conversion):
    """  Recursively converts dict keys based on passed in conversion function
    :param self:
    :param source:
    :param conversion:
    :return:
    """
    result = OrderedDict()
    for k in source:
        key = conversion(k)
        if isinstance(source[k], dict):
            result[key] = convert_dict(source[k], conversion)
        elif isinstance(source[k], list):
            result[key] = convert_list(source[k], conversion)
        else:
            result[key] = source[k]
    return result


def convert_list(source, conversion):
    """  Recursively converts list items based on passed in conversion function
    :param self:
    :param source:
    :param conversion:
    :return:
    """
    result = []
    for i in source:
        if isinstance(i, list):
            result.append(convert_list(i, conversion))
        elif isinstance(i, dict):
            result.append(convert_dict(i, conversion))
        else:
            result.append(i)
    return result


def to_camel_case(word, uppercase_first_letter=False):
    """ Convert strings to CamelCase.
    @param word: str to convert
    @param uppercase_first_letter: boolean True if first letter is upper
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), word)

    return word[0].lower() + to_camel_case(word, True)[1:]


def to_snake_case(word):
    """ Convert strings to snake_case.
    @param word: str to convert
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()
