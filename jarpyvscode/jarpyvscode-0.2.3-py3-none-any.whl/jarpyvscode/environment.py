"""Module providing information about the environment on the used dev computer."""

# Standard library:
import platform
import subprocess
import typing as t
from pathlib import Path


def type_of_python_environment(python_interpreter: Path) -> t.Optional[str]:
    """Determine type of environment for given Python interpreter.

    At first the function checks if a directory named ``conda-meta`` is a subdirectory
    of ``sys.prefix`` for the given *python_interpreter*. If that resolves to true
    this functions returns ``"conda"``.

    Parameters
    ----------
    python_interpreter
        Absolute path to a Python executable

    Returns
    -------
    t.Optional[str]
        None is returned when the type of Python environment cannot be determined.

        Otherwise ``conda`` oder `venv` will be returned.

    """
    _type: t.Optional[str] = None

    # check if *python_interpreter* belongs to a conda env:
    cmd: t.List[str] = [
        str(python_interpreter),
        "-c",
        (
            "import sys; from pathlib import Path; "
            "print('conda') "
            "if Path(sys.prefix, 'conda-meta').exists() "
            "else print('')"
        ),
    ]
    _type = subprocess.check_output(cmd, encoding="utf8")
    if _type is not None:
        _type = _type.replace("\r\n", "").replace("\n", "")
        if _type:
            return _type

    # code will continue here if *python_interpreter* does not belong to a conda env.

    # check if *python_interpreter* belongs to a venv:
    cmd = [
        str(python_interpreter),
        "-c",
        (
            "import sys; from pathlib import Path; "
            "print('venv') "
            "if Path(sys.prefix, 'pyvenv.cfg').exists() "
            "else print('')"
        ),
    ]
    _type = subprocess.check_output(cmd, encoding="utf8")
    if _type is not None:
        _type = _type.replace("\r\n", "").replace("\n", "")
        if _type:
            return _type
    return None


def operating_system() -> str:
    """Return an alias for the operating system.

    Returns
    -------
    str
        * ``"windows"`` for MS Windows systems
        * ``"osx"`` for macOS
        * ``"linux"`` for Linux

    """
    system = platform.system().lower()
    if system == "darwin":
        system = "osx"
    return system
