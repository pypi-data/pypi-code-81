"""Module defining constants used in the project."""

# Standard library:
import platform
import socket
import typing as t
from pathlib import Path

# 3rd party:
import psutil

ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"""Define capital letters of the alphabet."""


DOT_ENV_FILE_PATH: Path = Path(__file__).resolve().parents[1] / ".env"
"""Expected path to the location of an environment variable definition file."""


GIT_AUTHOR_RULES: t.Dict[str, t.Dict[str, str]] = {
    "gitlab\\.com[:/]jar1/": {
        "name": "Jamil Raichouni",
        "email": "raichouni@gmail.com",
    }
}
"""
Define rules for setting Git author details in ``.git/config`` files.

Applies, when

* a workspace is opened,
* the top folder of the workspace represents a Git reposiory, and
* the local Git config has no Git author configured.

These rules are considered by the function :func:`jarpyvscode.setups.set_git_user`.

"""


HOSTNAME: str = (
    socket.gethostname().split(".")[0].lower()
    if "." in socket.gethostname()
    else socket.gethostname().lower()
)
"""Lower-cased string upto the first ``"."`` (if existing) of the computer name."""


PROJECT_DIR: Path = Path(__file__).resolve().parents[1]
"""Absolute path to the root directory for the project."""


PROJECT_KIND_PYTHON: str = "Python"
"""Define name for a Python project."""


PROJECT_KIND_VSCE: str = "Visual Studio Code Extension"


PROJECT_NAME: str = PROJECT_DIR.name
"""Name of the project."""


PYTHON_PROJECT_ROOT_FILE_NAMES: t.Tuple[str, ...] = (
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "Pipfile.lock",
)

FRONTEND_DIR: Path = PROJECT_DIR / f"ui/dist/{PROJECT_NAME.replace('_', '-')}"
"""Absolute path to the Angular web application."""


DATA_DIR: Path = PROJECT_DIR / "data"
"""Absolute path to the data directory for the project."""


DATABASE_PATH: Path = DATA_DIR / f"{PROJECT_NAME}.db"
"""Absolute path to a SQLite database for the project."""


EXTENSION_NAME: str = "jarpyvscode"
"""Technical name of the extension ``JAR's pyVSCode``."""


EXTENSION_PUBLISHER: str = "jamilraichouni"
"""Name for the publisher of the Visual Studio Code extension ``JAR's pyVSCode``."""


PLATFORM_LOWER: str = platform.platform().lower()
"""
Define lower-cased platform name.

This value can be used to perform checks like

.. code-block:: python

    "linux" in PLATFORM_LOWER
    "macos" in PLATFORM_LOWER
    "windows" in PLATFORM_LOWER

"""


NICE_VALUE: int = (
    # if the windows val is changed, also maintain var 'prio_str' !!!
    psutil.ABOVE_NORMAL_PRIORITY_CLASS  # type: ignore # noqa attr ABOVE_NORMAL_PRIORITY_CLASS on win only
    if "windows" in PLATFORM_LOWER
    else -15
)
"""Define prioroty for Visual Studio Code processes."""


LOG_DIR: Path = (
    Path.home() / "Library/Logs/jarpyvscode"
    if "macos" in PLATFORM_LOWER
    else Path.home()
)
"""Absolute path to the log directory for the project."""


PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
"""Absolute path to the directory for processed data of the project."""


RAW_DATA_DIR: Path = DATA_DIR / "raw"
"""Absolute path to the directory for raw data of the project."""


SOFTWARE_VERSION_PATTERN: str = r"^(\d+|\d+\.\d+|\d+\.\d+\.\d+)$"
"""Define a RegEx for typical software version strings."""


TMP_DATA_DIR: Path = DATA_DIR / "tmp"
"""Absolute path to the directory for temporary data of the project."""
