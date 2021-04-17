"""Module with string functions."""

# Standard library:
import os
import re
import typing as t
from pathlib import Path

# local:
import jarpyvscode.constants as c
import jarpyvscode.paths

PLACEHOLDER_PATTERN = r"(?<=\$\{env:)(.*?)(?=\})"


def decompose_version(version: str) -> t.Dict[str, t.Optional[str]]:
    r"""Parse major and optionally minor and patch number from a version string.

    The string *version* will be stripped before it gets processed.

    Parameters
    ----------
    version
        A version string (e. g. ``"1.2.3"`` or ``"3.5"``) to parse.

    Returns
    -------
    t.Dict[str, t.Optional[str]]
        A dictionary with keys ``"major"``, ``"minor"``, and ``"patch"``.
        If *version* is not providing any minor or patch version information the
        according key values will be None.

    Raises
    ------
    TypeError
        If *version* is not a string.

    ValueError
        If *version* does not match the regular expression
        ``r"^(\d+|\d+\.\d+|\d+\.\d+\.\d+)$"``.

    Examples
    --------
    >>> decompose_version(version="1.2.3")
    {'major': '1', 'minor': '2', 'patch': '3'}

    >>> decompose_version(version="1.2")
    {'major': '1', 'minor': '2', 'patch': None}

    >>> decompose_version(version="1")
    {'major': '1', 'minor': None, 'patch': None}

    .. index::
        single: Version (decompose)

    """
    if not isinstance(version, str):  # type: ignore
        raise TypeError("The argument 'version' must be a string.")
    version = version.strip()
    if re.match(c.SOFTWARE_VERSION_PATTERN, version) is None:
        raise ValueError(
            "Cannot decompose software version information from " f"'{version}'!"
        )
    _version: t.Dict[str, t.Optional[str]] = {
        "major": None,
        "minor": None,
        "patch": None,
    }
    if "." in version:
        version_splitted = version.split(".")
        _version["major"] = version_splitted[0]
        _version["minor"] = version_splitted[1]
        if version.count(".") == 2:
            _version["patch"] = version_splitted[2]
    else:
        _version["major"] = version
    return _version


def fill_environment_variables(val: str) -> str:
    r"""Fill any potential ``${...}`` placeholders with value of environment variable.

    If the value of the environment variable contains a path pointing to an existing
    directory or file the separators of the path will be set as ``"\"`` (backslash).

    Parameters
    ----------
    val
        String value with potential placeholders to be populated by value of environment
        variable

    Returns
    -------
    str
        String value where any placeholders for existing environment variables have
        been populated by the environment variable's value.

    """
    match = re.findall(PLACEHOLDER_PATTERN, val)
    if match is not None:
        for name in match:
            env_var_val: str = os.getenv(name, "")
            if not env_var_val:
                continue
            if all(
                (
                    Path(env_var_val).is_dir() or Path(env_var_val).is_file(),
                    "windows" in c.PLATFORM_LOWER,
                )
            ):
                env_var_val = jarpyvscode.paths.path_backslashed(env_var_val)
            val = val.replace("${env:" + name + "}", env_var_val)
    return val


def fill_placeholders(subject: str, **kwargs: str) -> str:
    """Populate placeholders of format ``${PLACEHOLDER_NAME}`` in a template string.

    Parameters
    ----------
    subject
        A string containing named (keys of *kwargs*) placeholders ``${KEY}`` to be
        filled by values.

    kwargs
        Key/ value pairs with:

        * key: placeholder name
        * val: value for the placeholder to be filled

    Returns
    -------
    str
        Populated string

    Raises
    ------
    TypeError
        If *subject* is not a string.

    Examples
    --------
    >>> fill_placeholders("Hello ${SOMEBODY}!", {"SOMEBODY": "my friend"})
    'Hello my friend!'

    >>> version = {"MAJOR": "1", "MINOR": "2", "PATCH": "3"}
    >>> fill_placeholders("Version: ${MAJOR}.${MINOR}.${PATCH}", version)
    'Version: 1.2.3'

    """
    if not isinstance(subject, str):
        raise TypeError("The argument 'subject' must be a string.")
    if "${" not in subject:
        return subject
    for (key, val) in kwargs.items():
        place_holder = "${" + key + "}"
        if val is not None:
            subject = subject.replace(place_holder, val)
        else:
            subject = subject.replace(place_holder, "")
    return subject


if __name__ == "__main__":
    pass  # to avoid module execution by Sphinx extension autodoc
