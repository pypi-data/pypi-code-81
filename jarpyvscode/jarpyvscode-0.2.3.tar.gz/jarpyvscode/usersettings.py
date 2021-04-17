"""Module with tools to deal with (host-dependent) global user settings in VSCode."""

# Standard library:
import json
import typing as t
from operator import itemgetter
from pathlib import Path

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.jsonutils
import jarpyvscode.paths
import jarpyvscode.strings
from jarpyvscode.log import logger


def determine_applicability_score(host_setting: t.Dict[str, t.Any]) -> int:
    """Determine if a host_setting is applicable on the current host.

    Parameters
    ----------
    host_setting
        Setting from file ``host_settings.json``

    Returns
    -------
    int
        Applicability score (0-100) with

        100 : applicable specifically for the given host
        50  : applicable specifically for the given operating system and for all hosts
        10  : applicable on all operating systems and all hosts
        0   : not applicable

    """
    applicability_score: int = 0
    if not host_setting:
        return applicability_score
    elif any(
        (
            "hosts" not in host_setting,
            "os" not in host_setting,
        )
    ):
        return applicability_score
    hostname: str = c.HOSTNAME
    os: str = jarpyvscode.environment.operating_system()
    if any(
        (
            isinstance(host_setting["hosts"], str)
            and host_setting["hosts"] == hostname,
            isinstance(host_setting["hosts"], list)
            and hostname in host_setting["hosts"],
        )
    ):
        applicability_score = 100

    if not applicability_score and (
        (host_setting["hosts"] is None or hostname not in host_setting["hosts"])
        and host_setting["os"] is not None
        and any(
            (
                isinstance(host_setting["os"], str) and host_setting["os"] == os,
                isinstance(host_setting["os"], list) and os in host_setting["os"],
            )
        )
    ):
        applicability_score = 50

    if (
        not applicability_score
        and host_setting["hosts"] is None
        and host_setting["os"] is None
    ):
        applicability_score = 10

    return applicability_score


def jarroot() -> Path:
    """Determine host-specific path to the base directory for development.

    Read extension setting ``jarpyvscode.jarroot`` for the current host from the file
    ``host_settings.json`` (see :func:`jarpyvscode.paths.host_settings_path`).

    If the file ``host_settings.json`` does not exist or does not contain a setting
    ``jarpyvscode.jarroot`` that is applicable for the current host computer, the
    base directory will be set to the user’s home directory.

    Returns
    -------
    Path
        Path to the host-specific development base directory

    """
    host_settings: t.List[t.Dict[str, t.Any]]
    if not jarpyvscode.paths.host_settings_path().is_file():
        return Path.home()
    else:
        host_settings = read_host_settings()
        jarroot_settings: t.List[t.Dict[str, t.Any]] = [
            s for s in host_settings if "key" in s and s["key"] == "jarpyvscode.jarroot"
        ]
        if not jarroot_settings:
            return Path.home()
        for jarroot_setting in [j for j in jarroot_settings if j]:
            jarroot_setting["applicability_score"] = determine_applicability_score(
                jarroot_setting
            )
        jarroot_settings = sorted(
            jarroot_settings, key=itemgetter("applicability_score"), reverse=True
        )
        if jarroot_settings[0]["applicability_score"]:
            return Path(jarroot_settings[0]["val"])
        else:
            return Path.home()


def jarroots() -> t.List[Path]:
    """Determine dictionary of host-specific paths to base directories for development.

    Read all extension settings ``jarpyvscode.jarroot`` for all hosts from the file
    ``host_settings.json`` (see :func:`jarpyvscode.paths.host_settings_path`).

    If the file ``host_settings.json`` does not exist or does not contain a setting
    ``jarpyvscode.jarroot``, a dictionary with one key as defined by
    :const:`jarpyvscode.constants.HOSTNAME` and values as returned by
    :func:`jarpyvscode.paths.jarroot` will be returned.

    Returns
    -------
    Path
        Path to the host-specific development base directory

    """
    host_settings_file_path: Path = jarpyvscode.paths.host_settings_path()
    if not host_settings_file_path.is_file():
        logger.warning(
            f"Cannot find host-specific settings file '{host_settings_file_path}'!"
        )
        return [jarroot()]
    host_settings: t.List[t.Dict[str, t.Any]] = read_host_settings()
    jarroot_settings: t.List[t.Dict[str, t.Any]] = [
        s for s in host_settings if "key" in s and s["key"] == "jarpyvscode.jarroot"
    ]
    if not jarroot_settings:
        return [jarroot()]
    retval: t.List[Path] = list(
        set([Path(s["val"]) for s in jarroot_settings if "val" in s])
    )
    return retval


def possible_foreign_jarroots() -> t.List[Path]:
    """Return list of base directories for development on other computers.

    Returns
    -------
    t.List[Path]
        Unique list of all paths configured by the extension setting
        ``jarpyvscode.jarroot``.

    """
    _jarroot: Path = jarroot()
    _possible_foreign_jarroots: t.List[Path] = [r for r in jarroots() if r != _jarroot]
    _possible_foreign_jarroots = list(set(_possible_foreign_jarroots))
    return _possible_foreign_jarroots


def read_user_setting(
    key_chain: t.Union[str, t.Tuple[str, ...]]
) -> t.Optional[t.Union[bool, t.Dict[str, t.Any], float, int, str, t.List[t.Any]]]:
    """Read a setting value from the global user settings.

    This function reads a setting value from the global user settings file
    located at ``Code/User/settings.json``.

    A setting value according to the key name(s) (multiple for a nested setting)
    will be read.

    Parameters
    ----------
    key_chain
        Key name of tuple of key names for a nested setting.

    Returns
    -------
    t.Optional[t.Union[bool, dict, float, int, str, t.List[t.Any]]]
        Setting value or None, if the setting value is ``null`` or not given.

    """
    user_settings_path: Path = jarpyvscode.paths.user_settings_path()
    if not user_settings_path.is_file():
        logger.error(f"Cannot find the file {user_settings_path}!")
        return None
    if isinstance(key_chain, str):
        key_chain = (key_chain,)
    settings_str: str = user_settings_path.read_text()
    try:
        setting_val = json.loads(settings_str)
    except json.JSONDecodeError as e:
        logger.error(f"Cannot parse the file '{user_settings_path}': {str(e)}")
        return None
    considered_key_chain = []
    for key in key_chain:
        considered_key_chain.append(key)
        if key not in setting_val:
            considered_key_chain_str = "/".join(considered_key_chain)
            logger.error(
                f"Cannot find the setting {considered_key_chain_str} "
                f"in the file {user_settings_path}!"
            )
            return None
        setting_val = setting_val[key]
    return setting_val


def read_user_settings() -> t.Dict[str, t.Any]:
    """Read global (user) settings from ``User/settings.json``.

    Returns
    -------
    t.Dict[str, t.Any]
        Dictionary with user settings. This can be an empty dictionary when the file
        ``User/settings.json`` does not exist.

    Raises
    ------
    ValueError
        If an existing user settings file can not be read (invalid JSON).

    """
    settings: t.Dict[str, t.Any] = {}
    user_settings_path: Path = jarpyvscode.paths.user_settings_path()
    if not user_settings_path.is_file():
        return settings
    settings_str: str = user_settings_path.read_text()
    try:
        settings = json.loads(settings_str)
    except ValueError as e:
        # TODO: Shouldn't json.JSONDecodeError be caught?
        logger.error(f"Cannot parse the file '{user_settings_path}': {str(e)}")
    return settings


def read_host_settings() -> t.List[t.Dict[str, t.Any]]:
    """Read host-dependent global user settings.

    The settings are read from the file
    ``User/globalStorage/jamilraichouni.jarpyvscode/host_settings.json``.

    Returns
    -------
    t.List[t.Dict[str, t.Any]]
        List of dictionaries with host-dependent global user settings.
        This can be a list with one empty dictionary when the file
        ``host_settings.json`` does not exist.

    Raises
    ------
    ValueError
        If an existing host settings file can not be read (invalid JSON).

    """
    settings: t.List[t.Dict[str, t.Any]] = [{}]
    host_settings_path: Path = jarpyvscode.paths.host_settings_path()
    if not host_settings_path.exists():
        return [{}]
    settings_str: str = host_settings_path.read_text()
    try:
        settings = json.loads(settings_str)
    except ValueError as e:
        # TODO: Shouldn't json.JSONDecodeError be caught?
        logger.error(f"Cannot parse the file '{host_settings_path}': {str(e)}")
    return settings


def setup():
    """Set up user settings considering host-dependent configuration.

    Read host-dependent global user settings from the file
    ``Code/User/globalStorage/jamilraichouni.jarpyvscode/host_settings.json``.

    The algorithm iterates over all host settings and removes the setting from the
    global user settings if it is defined. Next the logic checks if a setting is
    applicable on the current host and if so, the setting will be introduced
    in the global user settings file ``Code/User/settings.json`` of VS Code.

    """
    try:
        user_settings: t.Optional[t.Dict[str, t.Any]] = read_user_settings()
        host_settings: t.List[t.Dict[str, t.Any]] = read_host_settings()
    except ValueError:
        return
    if any(
        (
            user_settings is None,
            host_settings is None,
            not host_settings,
        )
    ):
        return
    # is_dirty_user_settings: bool = False
    for host_setting in [h for h in host_settings if h]:
        host_setting["applicability_score"] = determine_applicability_score(
            host_setting
        )
        if user_settings is not None and host_setting["key"] in user_settings:
            del user_settings[host_setting["key"]]
            # is_dirty_user_settings = True

    host_settings = sorted(
        host_settings, key=itemgetter("applicability_score"), reverse=True
    )
    considered_keys = []
    for host_setting in [h for h in host_settings if h]:
        if host_setting["key"] in considered_keys:
            continue
        if host_setting["applicability_score"]:
            considered_keys.append(host_setting["key"])
            if isinstance(host_setting["val"], str):
                val = jarpyvscode.strings.fill_environment_variables(
                    host_setting["val"]
                )
            else:
                val = host_setting["val"]
            if user_settings is not None:
                user_settings[host_setting["key"]] = val
            # is_dirty_user_settings = True
    # if is_dirty_user_settings:
    user_settings_str = json.dumps(obj=user_settings, indent=4, sort_keys=True)
    val: t.Union[Path, str, int, float]
    for val in jarpyvscode.jsonutils.json_values_of_type_generator(
        json_info=user_settings,
        value_type=str,
    ):
        val = str(val)
        new_val = jarpyvscode.strings.fill_environment_variables(str(val))
        new_val = new_val.replace("\\\\", "~~|~~")  # store double backslashs
        new_val = new_val.replace("\\", "\\\\")  # replace single by double backslashs
        new_val = new_val.replace("~~|~~", "\\\\")  # restore double backslashs
        user_settings_str = user_settings_str.replace(f'"{val}"', f'"{new_val}"')

    user_settings_path: Path = jarpyvscode.paths.user_settings_path()
    user_settings_path.write_text(user_settings_str)


def write_host_settings(host_settings: t.List[t.Dict[str, t.Any]]):
    """Write host-dependent global user settings.

    The settings are written into the file
    ``User/globalStorage/jamilraichouni.jarpyvscode/host_settings.json``.

    Parameters
    ----------
    host_settings
        List of dictionaries with host-dependent global user settings.
        This can be a list with one empty dictionary.

    """
    host_settings_path: Path = jarpyvscode.paths.host_settings_path()
    if not host_settings_path.parent.is_dir():
        host_settings_path.parent.mkdir(parents=True)
    host_settings = sorted(host_settings, key=itemgetter("key"))
    host_settings_path.write_text(
        json.dumps(host_settings, sort_keys=True, indent=4) + "\n"
    )
