"""Module with tools dealing with virtual environments."""

# Standard library:
import json
import subprocess
import typing as t
from pathlib import Path

# 3rd party:
import pandas as pd

POETRY_VENV_NAME_PATTERN: str = r"^([\d\w\-_]{1,50})(-[\d\w]{8}-py.*)$"


def request_installed_package_versions_from_conda(
    prefix: Path,  # pkg_names: List[str] # noqa
) -> t.Optional[pd.DataFrame]:
    """Request installed package versions from conda for an environment prefix.

    Parameters
    ----------
    prefix
        Path to an existing conda environment

    Returns
    -------
    DataFrame or None
        List of installed packages with information or None, if an
        error occurs. The returned DataFrame contains the following columns:

        * ``name``
        * ``version``

    """
    raise NotImplementedError(
        "Code to request installed pkg versions from conda has been disabled. "
        "It can be copied from module jarlib.conda in repo "
        "https://gitlab.com/jar1/jar if needed."
    )
    # pkgs: t.Optional[pd.DataFrame] = jarlib.conda.environment.list_packages(
    #     prefix=prefix  # pkg_names=pkg_names
    # )
    # if pkgs is None:
    #     return
    # pkgs = pkgs.loc[:, ["name", "version"]]  # type: ignore
    # return pkgs


def request_installed_package_versions_from_pip(
    python_interpreter: Path,  # pkg_names: List[str]
) -> t.Optional[pd.DataFrame]:
    """Request installed package versions from pip for an ``venv`` environment prefix.

    Parameters
    ----------
    python_interpreter
        Absolute path to a Python executable that is expected to belong to a Python
        conda or venv environment.

    Returns
    -------
    DataFrame or None
        List of installed packages with information or None, if an
        error occurs. The returned DataFrame contains the following columns:

        * ``name``
        * ``version``

    """
    pkgs: t.Optional[pd.DataFrame] = None
    output: str = subprocess.check_output(
        [str(python_interpreter), "-m", "pip", "list", "--format", "json"],
        encoding="utf8",
    )
    pkg_json: t.List[t.Dict[str, str]] = json.loads(output)
    output = subprocess.check_output(
        [
            str(python_interpreter),
            "-c",
            "import sys;print('.'.join([str(i) for i in tuple(sys.version_info)[:3]]))",
        ],
        encoding="utf8",
    )
    output = output.replace("\r\n", "").replace("\n", "")
    pkg_json.append({"name": "python", "version": output})

    pkgs = pd.read_json(json.dumps(pkg_json))  # type: ignore
    if pkgs is None:
        return None
    return pkgs
