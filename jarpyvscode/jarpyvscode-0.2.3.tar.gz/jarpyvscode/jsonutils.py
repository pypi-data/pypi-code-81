"""Utilities to process JSON data."""

# Standard library:
import codecs
import sys
import typing as t
from os.path import isfile
from pathlib import Path

# special import setup:
try:
    # 3rd party:
    import json5 as json
except ImportError:
    # built-in:
    # Standard library:
    import json  # type: ignore

# local:
from jarpyvscode.log import logger


def json_string_replace(
    json_info: t.Union[str, t.Dict[str, t.Any]],
    key_chain: t.Tuple[str],
    old: str,
    new: str,
    encoding: str = "utf8",
) -> t.Optional[t.Union[t.Dict[str, t.Any], t.Any]]:
    """Replace a string in a string value of a JSON data/ file.

    Parameters
    ----------
    json_info
        Path to JSON file or JSON dictionary (loaded JSON data).
        If *json_info* is of type ``str`` it is assumed,
        that *json_info* is a path to a JSON file, otherwise and
        if *json_info* is of type ``dict`` it is assumed,
        that *json_info* is a loaded JSON dictionary.

    key_chain
        Chain of keys in JSON target pointing to string value to
        be manipulated.

    old
        String value to be replaced

    new
        String value to put inplace of ``old``.

    encoding : optional, the default is ``"utf8"``
        File encoding

    Returns
    -------
    t.Optional[t.Dict[str, t.Any]]
        None, if *json_info* is of type string,
        otherwise the processed JSON dictionary is being returned.

    """
    func_name = sys._getframe().f_code.co_name  # type: ignore
    json_data: t.Optional[t.Any] = None
    if isinstance(json_info, str):
        if not isfile(json_info):
            logger.error(f'{func_name}: Cannot find file "{json_info}"!')
            return None
        with codecs.open(json_info, "r", encoding) as json_file:
            json_data = json.load(json_file)
    elif isinstance(json_info, dict):
        json_data = json_info
    string_value = json_data
    if string_value is not None:
        key: str = ""
        string_value_parent_obj: t.Optional[t.Any] = None
        for key in key_chain:
            if not isinstance(string_value, dict) and not isinstance(string_value, str):
                logger.error(
                    f"{func_name}: Keychain {str(key_chain)} is not pointing to "
                    f"a string value in '{json_info}'!"
                )
                return None
            if isinstance(string_value, dict) and key in string_value:
                string_value_parent_obj = string_value
                string_value = string_value[key]
            else:
                logger.error(
                    f"{func_name}: Keychain {str(key_chain)} is not valid (given) "
                    f"for '{json_info}'!"
                )
                return None
        string_value = str(string_value).replace(old, new)
        if string_value_parent_obj is not None:
            string_value_parent_obj[key] = string_value

        if isinstance(json_info, str):
            with codecs.open(json_info, "w", encoding) as json_file:
                json.dump(
                    json_data,
                    json_file,
                    indent=4,
                    quote_keys=True,
                    trailing_commas=False,
                )
        elif isinstance(json_info, dict):
            return json_data
    return None


def json_values_of_type_generator(
    json_info: t.Union[Path, str, t.Dict[str, t.Any], t.List[t.Any]],
    value_type: t.Union[t.Type[float], t.Type[int], t.Type[str]],
    encoding: str = "utf8",
    _is_initial_call: bool = True,
) -> t.Generator[t.Union[Path, str, int, float], None, None]:
    """Return iterator for all values of a given data type in JSON file.

    Parameters
    ----------
    json_info:
        Path to JSON file or JSON dictionary (loaded JSON data).
        If *json_info* is of type ``str`` it is assumed,
        that *json_info* is a path to a JSON file, otherwise and
        if *json_info* is of type ``dict`` it is assumed,
        that *json_info* is a loaded JSON dictionary.

    value_type
        Expected basic Python data type for the type of values to get

    encoding : optional, the default is ``"utf8"``
        File encoding

    _is_initial_call

        .. warning:: This is an internal argument and should never be used.

        The argument is needed due to the recursive nature of the function.

    Yields
    ------
    t.Union[str, int, float]
        JSON value data

    """
    if all(
        (
            _is_initial_call,
            (
                (isinstance(json_info, str) and isfile(json_info))
                or (isinstance(json_info, Path) and json_info.is_file())
            ),
        )
    ):
        json_info = json.loads(Path(str(json_info)).read_text())
    if isinstance(json_info, dict):
        for _, val in json_info.items():
            yield from json_values_of_type_generator(
                val, value_type, encoding=encoding, _is_initial_call=False
            )
    elif isinstance(json_info, list):
        for item in json_info:
            yield from json_values_of_type_generator(
                item, value_type, encoding=encoding, _is_initial_call=False
            )
    else:
        if value_type == int:
            if not isinstance(json_info, bool) and isinstance(json_info, int):
                yield json_info
        elif isinstance(json_info, value_type):
            yield json_info
