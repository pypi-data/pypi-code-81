"""
A collection of useful string utilities.
"""
from typing import Optional

# Strings representing boolean values
TRUE_STRINGS = ('y', 'yes', 't', 'true', 'on', '1')
FALSE_STRINGS = ('n', 'no', 'f', 'false', 'off', '0')
BOOL_STRINGS = TRUE_STRINGS + FALSE_STRINGS

# default value of that's considered 'SHORT'
SHORT_STRING_LEN = 64


def trim(value, default_value='') -> Optional[str]:
    """
    Removes leading and trailing whitespace from the specified string. If the specified string is an empty
    string, ``None`` or a string composed of whitespace only, the specified default value is returned.

    :param value: a string to trim.
    :param default_value: a default value to return if the specified string is empty or consists of whitespace only.
    :return: a string without any leading or trailing whitespace or the specified default value if
        the specified string is an empty string, ``None`` or a string composed of whitespace only.
    """
    value = value.strip() if value else None
    return value if value else default_value


def ensure_not_blank(value, message=None):
    """
    Removes leading and trailing whitespace from the specified string and checks whether or not
    it is blank (None or whitespace). If it is, it raises a `ValueError` with the specified `message`.

    :param value: value to check
    :param message: message to pass to ValueError
    :raises ValueError
    """
    message = message if message else "Value must not be blank"
    value = trim(value)
    if value:
        return value
    else:
        raise ValueError(message)


def trim_to_lower(value, default_value=''):
    """
    Removes leading and trailing whitespace from the specified string and converts it to lowercase.
    If the specified string is empty, ``None`` or composed of whitespace only, the specified default
    value is returned. If the default value is returned and it is a non-empty string, it is also
    converted to lowercase.

    :param value: a string to trim and convert to lowercase.
    :param default_value: a default value to return if the specified string is empty or consists of whitespace only.
    :return: a lowercase string without any leading or trailing whitespace or the specified default value if
        the specified string is an empty string, ``None`` or a string composed of whitespace only.
    """
    res = trim(value, default_value)
    return res if res is None else res.lower()


def trim_to_upper(value, default_value=''):
    """
    Removes leading and trailing whitespace from the specified string and converts it to uppercase.
    If the specified string is empty, ``None`` or composed of whitespace only, the specified default
    value is returned. If the default value is returned and it is a non-empty string, it is also
    converted to uppercase.

    :param value: a string to trim and convert to uppercase.
    :param default_value: a default value to return if the specified string is empty or consists of whitespace only.
    :return: an uppercase string without any leading or trailing whitespace or the specified default value if
        the specified string is an empty string, ``None`` or a string composed of whitespace only.
    """
    res = trim(value, default_value)
    return res if res is None else res.upper()


def combine_url(base_url, *args):
    """Combines the base url and the path component, taking care of the slashes"""
    parts = [base_url, *args]
    return '/'.join(s.strip('/') for s in parts)


def string_2_bool(value) -> bool:
    """
    Extracts boolean value from a string in a case insensitive manner. This method recognizes the following
    as valid boolean values:

        * true and false
        * 1 and 0
        * yes and no
        * on and off

    :param value: a value to convert to boolean
    :return: True or False
    :raises: ValueError if the string is not one of the known values.
    :rtype: bool
    """
    value = trim_to_lower(value)
    if value in TRUE_STRINGS:
        return True
    elif value in FALSE_STRINGS:
        return False
    else:
        raise ValueError(f'The value must be one of {BOOL_STRINGS}')


def truncate_long_text(long_text, max_len=SHORT_STRING_LEN):
    """Reduces an excessively long descriptions to approx. SHORT_STRING_LEN number of characters"""
    long_text = trim(long_text)
    if long_text:
        ellipses = '...'
        adjusted_max_len = max_len + len(ellipses)
        long_text = (long_text[:max_len] + ellipses) if len(long_text) > adjusted_max_len else long_text
    return long_text
