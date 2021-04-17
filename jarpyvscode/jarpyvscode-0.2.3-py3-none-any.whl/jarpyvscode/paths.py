"""Module with utilities to deal with folder/ file paths."""

# Standard library:
import itertools
import os
import typing as t
from pathlib import Path

# local:
import jarpyvscode.constants as c
import jarpyvscode.insiders


def code_dir() -> Path:
    r"""Return the path to location for the Visual Studio Code configuration.

    The location of the directory depends on the kind of Visual Studio Code
    (stable or insiders build), the operating system and the user name.

    **macOS**

    ``~/Library/Application Support/Code``
    ``~/Library/Application Support/Code - Insiders``

    **Linux:**

    ``~/.config/Code``
    ``~/.config/Code - Insiders``

    **Windows:**

    ``%APPDATA%\Code``
    ``%APPDATA%\Code - Insiders``

    Returns
    -------
    Path
        Path (separator will be ``"/"``) to the directory where the
        Visual Studio Code configuration is located

    """
    base_dir: Path = Path()
    if "linux" in c.PLATFORM_LOWER:
        base_dir = Path.home() / ".config"
    elif "macos" in c.PLATFORM_LOWER:
        base_dir = Path.home() / "Library/Application Support"
    elif "windows" in c.PLATFORM_LOWER:
        base_dir = Path(os.getenv("APPDATA", str(Path.home() / "AppData/Roaming")))
    if jarpyvscode.insiders.is_insiders():
        return Path(normalise_path(Path(base_dir / "Code - Insiders")))
    else:
        return Path(normalise_path(Path(base_dir / "Code")))


def extension_global_storage_dir() -> Path:
    """Path to the global storage directory of the Visual Studio extension.

    Returns
    -------
    Path
        Path (separator will be ``"/"``) to the directory where the
        global storage for the Visual Studio Code extension is located

    """
    return user_dir() / "globalStorage" / f"{c.EXTENSION_PUBLISHER}.{c.EXTENSION_NAME}"


def fix_doubled_drive_letter(string: str) -> str:
    """Fix doubled drive letter in ``string``.

    Replace

    * ``"C:C:"`` by ``"C:"``,
    * ``"C%3AC%3A"`` by ``"C%3A"``,
    * ``"B:B:"`` by ``"B:"``,
    * ``"B%3AB%3A"`` by ``"B%3A"``,

    etc. for all (upper and lower case) characters from the alphabet.

    Parameters
    ----------
    string
        String to fix

    Returns
    -------
    str
        Fixed string

    Examples
    --------
    >>> fix_doubled_drive_letter(string="C:C:")
    'C:C:'

    >>> fix_doubled_drive_letter(string="C:C%3A")
    'C:C:'

    >>> fix_doubled_drive_letter(string="d%3AD:")
    'C:C:'

    """
    char: str
    for char in c.ALPHABET:
        letter_variants = (char, char.lower())
        colon_variants = (":", "%3A")

        letter_combinations = list(itertools.product(letter_variants, repeat=2))
        colon_combinations = list(itertools.product(colon_variants, repeat=2))
        index_combinations = list(itertools.permutations((0, 1)))

        doubled_drive_letter_combinations = []

        for letter_combination in letter_combinations:
            for colon_combination in colon_combinations:
                for index_combination in index_combinations:
                    letter_0 = letter_combination[index_combination[0]]
                    letter_1 = letter_combination[index_combination[1]]

                    colon_0 = colon_combination[index_combination[0]]
                    colon_1 = colon_combination[index_combination[1]]

                    doubled_drive_letter_combination = (
                        f"{letter_0}{colon_0}{letter_1}{colon_1}"
                    )
                    doubled_drive_letter_combinations.append(
                        doubled_drive_letter_combination
                    )

        doubled_drive_letter_combinations = list(set(doubled_drive_letter_combinations))
        for doubled_drive_letter_combination in doubled_drive_letter_combinations:
            if doubled_drive_letter_combination in string:
                string = string.replace(doubled_drive_letter_combination, f"{char}:")
    return string


def host_settings_path() -> Path:
    """Path to the host-specific settings file.

    Returns
    -------
    Path
        Path to the host-specific settings file ``host_settings.json``

    """
    return extension_global_storage_dir() / "host_settings.json"


def normalise_path(path_string: t.Union[Path, str]) -> str:
    r"""Normalise path(s).

    Replace all occurences of ``"\"`` and ``"\\"`` by ``"/"`` and
    replace ``"%3A"`` by ``":"``.

    If *path_string* represents an MS Windows path, the drive
    letter will be capitalised.

    .. note::

        Leading backslashs won't be replaced if *path_string*
        starts with ``"\\"``.

    Parameters
    ----------
    path_string
        String containing path(s) or a path

    Returns
    -------
    str
        Normalised path

    """
    if isinstance(path_string, Path):
        path_string = str(path_string)
    if path_string.startswith("\\\\"):
        path_string = path_string.replace("\\\\", "~~~~", 1)
    protocols = ("file", "ftp", "http", "sftp")
    for protocol in protocols:
        path_string = path_string.replace(
            "{}://".format(protocol), "{}_DUMMY_DUMMY".format(protocol), 1
        )
    # backslashs --> forwardslashs:
    path_string = path_string.replace("\\", "/")
    path_string = path_string.replace("//", "/")
    path_string = path_string.replace("~~~~", "\\\\")
    for protocol in protocols:
        path_string = path_string.replace(
            "{}_DUMMY_DUMMY".format(protocol), "{}://".format(protocol), 1
        )
    path_string = path_string.replace(r"%3A", ":")
    char: str
    for char in c.ALPHABET:
        if path_string.startswith("{}:".format(char.lower())):
            path_string = path_string.replace(
                "{}:".format(char.lower()), "{}:".format(char)
            )
    return path_string


def path_backslashed(path_string: t.Union[Path, str]) -> str:
    r"""Use backslash (``"\"``) as path separator in path(s).

    Parameters
    ----------
    path_string
        String containing path(s) or a path

    Returns
    -------
    str
        Path with backslash as separator to split path components

    """
    if isinstance(path_string, Path):
        path_string = str(path_string)
    path_string = path_string.replace("/", "\\")
    path_string = path_string.replace("\\\\", "\\")
    return path_string


def path_double_backslashed(path_string: str) -> str:
    r"""Use double backslash (``"\\"``) as path separator in path(s).

    Parameters
    ----------
    path_string
        String containing path(s) or a path

    Returns
    -------
    str
        Path with double backslash as separator to split path components

    """
    # Replace all double backslashs:
    path_string = path_string.replace("\\\\", "\\")

    # Replace all single backslashs with double backslashs:
    path_string = path_string.replace("\\", "\\\\")

    # Replace all double forwardslashs with single forwardslashs:
    path_string = path_string.replace("//", "/")

    # Replace all single forwardslashs with double backslashs:
    path_string = path_string.replace("/", "\\\\")

    return path_string


def path_lower_drive_letter(path_string: str) -> str:
    """Make drive letter of path lower-cased.

    Parameters
    ----------
    path_string
        Path from which the drive letter is to be lower-cased.

    Returns
    -------
    str
        A string that is is *path_string* with a lower-cased the drive letter

    Examples
    --------
    >>> path_lower_drive_letter(path_string="C:/tmp")
    'c:/tmp'

    >>> path_lower_drive_letter(path_string="C%3A/tmp")
    'c%3A/tmp'

    """
    new_path = path_string

    protocols = ("file", "ftp", "http", "https", "sftp")
    for protocol in protocols:
        new_path = new_path.replace(f"{protocol}://", f"{protocol}_DUMMY_DUMMY")

    char: str
    for char in c.ALPHABET:
        old_drive_variants = (
            "{}:".format(char),
            r"{}%3A".format(char),
        )
        new_drive_variants = (
            "{}:".format(char.lower()),
            r"{}%3A".format(char.lower()),
        )
        for (old, new) in zip(old_drive_variants, new_drive_variants):
            if old in new_path:
                new_path = new_path.replace(old, new, 1)
                break
    for protocol in protocols:
        new_path = new_path.replace(
            "{}_DUMMY_DUMMY".format(protocol), "{}://".format(protocol), 1
        )
    return new_path


def path_remove_drive_letter(path_string: t.Union[Path, str]) -> str:
    """Remove drive letter from path.

    Parameters
    ----------
    path_string
        Path from which the drive letter and colon is to be removed.

    Returns
    -------
    str
        String that is *path_string* without the drive letter and colon

    Examples
    --------
    >>> path_remove_drive_letter(path_string="C:/tmp")
    '/tmp'

    >>> path_remove_drive_letter(path_string="C%3A/tmp")
    '/tmp'

    """
    if isinstance(path_string, Path):
        path_string = str(path_string)
    new_path = path_string

    protocols = ("file", "ftp", "http", "https", "sftp")
    for protocol in protocols:
        new_path = new_path.replace(f"{protocol}://", f"{protocol}_DUMMY_DUMMY")
        if new_path.startswith(protocol):
            break

    # for c in c.ALPHABET:
    c: str
    for c in [
        "C",
    ]:
        drive_variants = (
            rf"{c}%3A:",
            rf"{c.lower()}%3A:",
            f"{c}:",
            f"{c.lower()}:",
        )
        for drive_variant in drive_variants:
            break_drive_variant_loop = False
            if new_path.startswith(drive_variant):
                new_path = new_path.replace(drive_variant, "", 1)
                break_drive_variant_loop = True
                break
            for protocol in protocols:
                if new_path.startswith(f"{protocol}_DUMMY_DUMMY{drive_variant}"):
                    new_path = new_path.replace(drive_variant, "", 1)
                    break_drive_variant_loop = True
                    break
            if break_drive_variant_loop:
                break
        for protocol in protocols:
            new_path = new_path.replace(f"{protocol}_DUMMY_DUMMY", f"{protocol}://")
    return new_path


def user_dir() -> Path:
    r"""Return the path to location for the Visual Studio Code user configuration.

    The location of the directory depends on the kind of Visual Studio Code
    (stable or insiders build), the operating system and the user name.

    **macOS**

    ``~/Library/Application Support/Code/User``
    ``~/Library/Application Support/Code - Insiders/User``

    **Linux:**

    ``~/.config/Code/User``
    ``~/.config/Code - Insiders/User``

    **Windows:**

    ``%APPDATA%\Code\User``
    ``%APPDATA%\Code - Insiders\User``

    Returns
    -------
    Path
        Path (separator will be ``"/"``) to the directory where the
        Visual Studio Code user configuration is located

    """
    return code_dir() / "User"


def user_settings_path() -> Path:
    """Path to the global (user) settings file.

    Returns
    -------
    Path
        Path to the global (user) settings file ``settings.json``

    """
    return user_dir() / "settings.json"


def workspace_cfgs_dir() -> Path:
    r"""Return the path to the directory where ``.code-workspace`` files are located.

    The location of the directory depends on the kind of Visual Studio Code
    (stable or insiders build), the operating system and the user name.

    **macOS**

    ``~/Library/Application Support/Code/User/globalStorage/jamilraichouni.jarpyvscode/workspaces``
    ``~/Library/Application Support/Code - Insiders/User/globalStorage/jamilraichouni.jarpyvscode/workspaces``

    **Linux:**

    ``~/.config/Code/User/globalStorage/jamilraichouni.jarpyvscode/workspaces``
    ``~/.config/Code - Insiders/User/globalStorage/jamilraichouni.jarpyvscode/workspaces``

    **Windows:**

    ``%APPDATA%\Code\User\globalStorage\jamilraichouni.jarpyvscode\workspaces``
    ``%APPDATA%\Code - Insiders\User\globalStorage\jamilraichouni.jarpyvscode\workspaces``

    Returns
    -------
    Path
        Path to the directory where ``.code-workspace`` files are located

    """  # noqa
    return code_dir() / "User/globalStorage/jamilraichouni.jarpyvscode/workspaces"
