"""Module with tools dealing with assets used in VSCode.

Assets are defined in the global storage file ``assets.json`` which is used
by the Visual Studio Code extension ``jamilraichouni.jarpyvscode``.

"""
# Standard library:
import re
import typing as t
from pathlib import Path

# 3rd party:
import json5
import pandas as pd

# local:
import jarpyvscode.environment
import jarpyvscode.strings
import jarpyvscode.venvs
from jarpyvscode.log import logger

PLACEHOLDER_PATTERN = r".*?\$\{(MAJOR|MINOR|PATCH)\}.*"


def decomposed_package_version(
    pkgs: t.Optional[pd.DataFrame], pkg_name: str
) -> t.Optional[t.Dict[str, t.Optional[str]]]:
    """Return decomposed version information for a specified Python package.

    Parameters
    ----------
    pkgs
        DataFrame with two columns ``"name"`` and ``"version"`` for Python
        packages installed in a conda environment

    pkg_name
        Name of a Python package for which this function checks, if it is listed in
        *pkgs*.

    Returns
    -------
    t.Dict[str, t.Optional[str]]
        If the package named *pkg_name* is listed in *pkgs* a dictionary with decomposed
        version information will be returned.

        .. seealso:: :func:`jarpyvscode.strings.decompose_version`

    """
    if pkgs is None:
        return None
    f = pkgs["name"] == pkg_name
    pkg = pkgs.loc[f]
    if pkg.empty:
        return None
    version = jarpyvscode.strings.decompose_version(version=pkg.iloc[0].version)
    version_upper = {}
    for k, v in version.items():
        version_upper[k.upper()] = v
    return version_upper


def fill_template_asset(
    template_asset: t.Dict[str, t.Optional[str]], pkgs: t.Optional[pd.DataFrame] = None
) -> t.Dict[str, t.Optional[str]]:
    """Fill any potential ``${...}`` placeholders in asset template.

    Parameters
    ----------
    template_asset
        Asset object (dictionary) with potential ``${...}`` placeholders
        to be filled

    pkgs : optional
        DataFrame with two columns ``"name"`` and ``"version"`` for Python
        packages installed in a conda environment

    Returns
    -------
    t.Dict[str, t.Optional[str]]
        Asset object (dictionary) where potential ``${...}`` placeholders
        have been filled

    """
    if template_asset["type"] != "Website":
        return template_asset

    if re.match(PLACEHOLDER_PATTERN, str(template_asset["file_name_or_url"])) is None:
        return template_asset

    if template_asset["pkg_name"] is not None:
        # pkg_name is given:
        decomposed_installed_version: t.Optional[
            t.Dict[str, t.Optional[str]]
        ] = decomposed_package_version(
            pkgs=pkgs, pkg_name=str(template_asset["pkg_name"])
        )
        version: t.Dict[str, t.Optional[str]]
        k: str
        v: t.Optional[str]
        if decomposed_installed_version is None:
            # conda version not found:
            if template_asset["version"] is None:
                # conda version not found & "version" NOT given:
                template_asset["file_name_or_url"] = template_asset["fallback_url"]
            else:
                # conda version not found & "version" given:
                version = jarpyvscode.strings.decompose_version(
                    version=str(template_asset["version"])
                )
                version_upper: t.Dict[str, str] = {}
                for k, v in version.items():
                    if v is not None:
                        version_upper[k.upper()] = v
                template_asset[
                    "file_name_or_url"
                ] = jarpyvscode.strings.fill_placeholders(
                    subject=str(template_asset["file_name_or_url"]), **version_upper
                )
        else:
            # conda version found:
            template_asset["file_name_or_url"] = jarpyvscode.strings.fill_placeholders(
                subject=str(template_asset["file_name_or_url"]),
                **decomposed_installed_version,  # type: ignore
            )
        return template_asset

    # pkg_name NOT given:
    if template_asset["version"] is None:
        # "version" NOT given:
        template_asset["file_name_or_url"] = template_asset["fallback_url"]
    else:
        # "version" given:
        version = jarpyvscode.strings.decompose_version(
            version=str(template_asset["version"])
        )
        version_upper = {}
        for k, v in version.items():
            if v is not None:
                version_upper[k.upper()] = v
        template_asset["file_name_or_url"] = jarpyvscode.strings.fill_placeholders(
            subject=str(template_asset["file_name_or_url"]), **version_upper
        )
    return template_asset


def fill_template_assets(
    python_interpreter: Path, template_assets: t.List[t.Dict[str, t.Optional[str]]]
) -> t.List[t.Dict[str, t.Optional[str]]]:
    """Fill ``${...}`` placeholders in list of asset templates.

    Parameters
    ----------
    python_interpreter
        Absolute path to a Python executable that is expected to belong to a Python
        conda or venv environment. Installed packages will be
        read from this environment to fill

        * ``${MAJOR}``,
        * ``${MINOR}``, and
        * ``${PATCH}``

        placeholders in the *template_assets* data according the installed version
        of the package defined by the assets key ``"pkg_name"``.

    template_assets
        List of asset objects (dictionaries) with potential ``${...}`` placeholders
        to be filled

    Returns
    -------
    t.List[t.Dict[str, t.Optional[str]]]
        List of asset objects (dictionaries) with filled ``${...}`` placeholders

    """
    is_request_for_installed_pkg_versions_needed: bool = bool(
        [
            template_asset
            for template_asset in template_assets
            if all(
                (
                    template_asset["type"] == "Website",
                    template_asset["pkg_name"] is not None,
                    re.match(
                        PLACEHOLDER_PATTERN,
                        str(template_asset["file_name_or_url"]),
                    )
                    is not None,
                )
            )
        ]
    )
    pkgs: t.Optional[pd.DataFrame] = None
    if is_request_for_installed_pkg_versions_needed:
        type_of_python_env: t.Optional[
            str
        ] = jarpyvscode.environment.type_of_python_environment(
            python_interpreter=python_interpreter
        )
        if type_of_python_env is not None:
            if type_of_python_env == "conda":
                raise NotImplementedError(
                    "Code to request installed pkg versions from conda has been "
                    "disabled. It can be copied from module jarlib.conda in repo "
                    "https://gitlab.com/jar1/jar if needed."
                )
                # # Get conda prefix:
                # conda_prefix: t.Optional[Path] = None
                # try:
                #     conda_prefix = jarlib.conda.environment.prefix(
                #         interpreter=python_interpreter
                #     )
                # except FileNotFoundError as e:
                #     logger.warning(str(e))
                #     return []
                # pkgs = jarlib.venvs.request_installed_package_versions_from_conda(
                #     prefix=Path(str(conda_prefix)),
                # )
            elif type_of_python_env == "venv":
                pkgs = jarpyvscode.venvs.request_installed_package_versions_from_pip(
                    python_interpreter=python_interpreter
                )
    assets: t.List[t.Dict[str, t.Optional[str]]] = []
    if pkgs is not None and not pkgs.empty:
        for template_asset in template_assets:
            assets.append(fill_template_asset(template_asset=template_asset, pkgs=pkgs))
    return assets


def read_template(
    template_file_path: Path,
) -> t.Optional[t.List[t.Dict[str, t.Optional[str]]]]:
    """Read template assets file that possibly contains ``${...}`` placeholders.

    Parameters
    ----------
    template_file_path
        Path to the template assets file

    Returns
    -------
    t.Optional[t.Dict[str, t.Optional[str]]]
        Dictionary with JSON data for template assets if no parsing error occurs

    """
    template_assets_str: str = template_file_path.read_text(encoding="utf8")
    template_assets: t.Optional[t.List[t.Dict[str, t.Optional[str]]]] = None
    try:
        template_assets = json5.loads(template_assets_str, encoding="utf8")
    except ValueError as e:
        logger.error(f"Cannot parse the file '{template_file_path}': {str(e)}")
    return template_assets


def setup(**kwargs: str) -> None:
    """Set up assets for the VSCode extension ``jamilraichouni.jarpyvscode``.

    The function takes a Python interpreter path and if the interpreter belongs to a
    Python environment (``conda`` or ``venv``), the function will populate
    any ``${MAJOR}``, ``${MINOR}``, or ``${PATCH}`` placeholders found in a specified
    assets template file with according installed Python package versions.

    Parameters
    ----------
    kwargs
        Key/ value pairs with:

        * Key: *python_interpreter*

          Val:

          Path to a Python interpreter for which this function tries to identify a
          corresponding conda environment prefix and requests installed package versions

        * Key: *input*

          Val: Path to input file of assets with placeholders

          * ``${MAJOR}``,
          * ``${MINOR}``, and
          * ``${PATCH}``

          to be populated. The populated version of the input file will be stored as a
          separate file with a path defined in *output* (see below).

        * Key: *output*

          Val: Path to the output file where the placeholders described above
          have been filled with according values.

    Raises
    ------
    ValueError
        If any of the keys ``"python_interpreter"``, ``"input"``, or ``"output"`` are
        not part of *kwargs*.

    FileNotFoundError
        If the file specified in *input* can not be found

    """
    # Check args:
    if any(
        (
            "python_interpreter" not in kwargs,
            "input" not in kwargs,
            "output" not in kwargs,
        )
    ):
        raise ValueError("Invalid arguments.")

    logger.info("Received the following arguments:")
    logger.info(f"\tPYTHON_INTERPRETER: \"{kwargs['python_interpreter']}\"")
    logger.info(f"\tINPUT: \"{kwargs['input']}\"")
    logger.info(f"\tOUTPUT: \"{kwargs['output']}\"")

    input_file: Path = Path(kwargs["input"])
    if not input_file.exists():
        raise FileNotFoundError(f"The file '{input_file}' cannot be found.")

    # Read assets from template file:
    template_assets: t.Optional[t.List[t.Dict[str, t.Optional[str]]]] = read_template(
        template_file_path=input_file
    )
    if template_assets is None:
        return

    # Check if the assets in the template contain any Website with placeholders to see,
    # if we need to request versions for installed packages in the conda environment:
    is_filling_template_needed: bool = bool(
        [
            template_asset
            for template_asset in template_assets
            if all(
                (
                    template_asset["type"] == "Website",
                    re.match(
                        r".*?\$\{(MAJOR|MINOR|PATCH)\}.*",
                        str(template_asset["file_name_or_url"]),
                    )
                    is not None,
                )
            )
        ]
    )
    assets: t.List[t.Dict[str, t.Optional[str]]]
    if is_filling_template_needed:
        python_interpreter: Path = Path(kwargs["python_interpreter"])
        assets = fill_template_assets(
            python_interpreter=python_interpreter, template_assets=template_assets
        )
    else:
        assets = template_assets

    write_assets_file(assets=assets, assets_file_path=Path(kwargs["output"]))


def write_assets_file(
    assets: t.List[t.Dict[str, t.Optional[str]]], assets_file_path: Path
) -> None:
    """Write filled assets (JSON data) into specified file.

    Parameters
    ----------
    assets
        List of asset objects (dictionaries) with filled ``${...}`` placeholders

    assets_file_path
        Path to the output file to be written

    Raises
    ------
    NotADirectoryError
        If the parent directory for the specified output file *assets_file_path* does
        not exist.

    """
    if not assets_file_path.parent.exists():
        raise NotADirectoryError(
            f"The parent directory for the specified output file '{assets_file_path}' "
            "cannot be found."
        )
    assets_file_path.write_text(
        data=json5.dumps(
            obj=assets, indent=2, sort_keys=True, quote_keys=True, trailing_commas=False
        ),
        encoding="utf8",
    )
