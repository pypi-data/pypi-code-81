"""Utilities for the VSCode wrapper and utility tool."""

# Standard library:
import getpass
import json
import os
import re
import typing as t
from collections import OrderedDict
from os.path import isdir, isfile, join
from pathlib import Path
from subprocess import PIPE, Popen

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.insiders
import jarpyvscode.paths
import jarpyvscode.usersettings
from jarpyvscode.log import logger


def adapt_jarroot_in_path(
    old_path: t.Union[Path, str], colon_str: str = ":", sep: str = "/"
) -> str:
    r"""Ensure valid base dir in path if any possible base dir is part of *old_path*.

    Search *old_path* and check, if any of the entries in the list returned by
    :func:`jarpyvscode.usersettings.possible_foreign_jarroots` (except the one that is
    returned by :func:`jarpyvscode.usersettings.jarroot`) appears in *old_path* and
    replace any finding by the value returned by
    :func:`jarpyvscode.usersettings.jarroot`.

    Set the path separator as specified via the argument *sep*.

    **On Windows systems:**

    Set the representation for the colon after the drive letter
    as specified by the argument *colon_str*.

    Parameters
    ----------
    old_path
        Path to update
    colon_str
        Representation of the colon for a path on a MS Windows
        computer. Possible values are ``":"`` and ``r"%3A"``.

        .. note:: This argument is considered on MS Windows only.
    sep
        Path separator for new value of path. Possible values are:

        * ``"/"``,
        * ``r"\"``, and
        * ``r"\\"``.

        .. note:: This argument is considered on MS Windows only.

    Returns
    -------
    str
        string with valid JARROOT if needed

    """
    if isinstance(old_path, Path):
        old_path = str(old_path)
    new_path = None
    _possible_foreign_jarroots: t.List[str] = [
        str(p) for p in jarpyvscode.usersettings.possible_foreign_jarroots()
    ]
    _jarroot = str(jarpyvscode.usersettings.jarroot())
    missing_jarroots: t.List[str] = []
    possible_jarroots = list(
        set(_possible_foreign_jarroots).difference(set([_jarroot]))
    )
    for possible_jarroot in possible_jarroots:
        possible_jarroot_normalised: str = jarpyvscode.paths.normalise_path(
            possible_jarroot
        )
        if possible_jarroot_normalised not in possible_jarroots:
            missing_jarroots.append(possible_jarroot_normalised)
    possible_jarroots += missing_jarroots
    protocols = ("file", "ftp", "http", "https", "sftp")
    old_path_normalised = jarpyvscode.paths.normalise_path(old_path)
    for possible_jarroot in possible_jarroots:
        condition_1: bool = (
            f"{jarpyvscode.paths.normalise_path(possible_jarroot)}/"
            in old_path_normalised
        )
        condition_2: bool = f"{possible_jarroot}/" in old_path_normalised.replace(
            r"%USERNAME%", getpass.getuser()
        )
        condition_3: bool = old_path_normalised == possible_jarroot
        if any(
            (
                condition_1,
                condition_2,
                condition_3,
            )
        ):
            old_path = jarpyvscode.paths.normalise_path(old_path)
            new_path = old_path.replace(f"{possible_jarroot}\\", f"{str(_jarroot)}\\")
            new_path = new_path.replace(f"{possible_jarroot}/", f"{str(_jarroot)}/")
            new_path = new_path.replace(
                f"{jarpyvscode.paths.normalise_path(possible_jarroot)}/",
                f"{str(_jarroot)}/",
            )
            # Next fix is needed in cases like the following:
            # old_path contains 'C:/Users/USER/repos/cdm'
            # possible_jarroot_variant equals '/Users/USER'
            # this leads to new_path = 'C:C:/Users/USER/repos/cdm'
            # Hence, we must replace 'C:C:' by 'C:' etc.
            new_path = jarpyvscode.paths.fix_doubled_drive_letter(new_path)
            if "windows" in c.PLATFORM_LOWER:
                if colon_str != ":":
                    for protocol in protocols:
                        new_path = new_path.replace(
                            f"{protocol}://", f"{protocol}_DUMMY_DUMMY", 1
                        )

                    new_path = new_path.replace(":", colon_str)

                    for protocol in protocols:
                        new_path = new_path.replace(
                            f"{protocol}_DUMMY_DUMMY", f"{protocol}://", 1
                        )
                if sep != "/":
                    new_path = new_path.replace("/", sep)
            else:
                new_path = jarpyvscode.paths.path_remove_drive_letter(new_path)
                if new_path.startswith("//"):
                    new_path = new_path[1:]
                if "file:////" in new_path:
                    new_path = new_path.replace("file:////", "file:///")
    if new_path is None:
        new_path = old_path
    return new_path


def alive(print_to_stdout: bool = True) -> bool:
    """Check, if VSCode is running.

    If VSCode is running and *stdout* is true (the default) the function will print 1
    otherwise 0.
    The printed value can be understood in Shell scripts calling

    .. code-block:: bash

        python vscode.py alive

    Implications:

    When a shell script calls ``python ${JARROOT}/repos/vscode launch [FILE]``
    and VSCode is not running (return value of 0 for this function) the launch
    of VSCode will require administrative permissions (call via sudo) to be able
    to set VSCode process priorities.

    The current function is being called from :func:`jarpyvscode.core.launch`.

    Parameters
    ----------
    print_to_stdout : optional
        If true (the default), the result will be printed to standard out.

    Returns
    -------
    bool
        True if VSCode is running, else False

    """
    vscode_search_string_lw = ""
    if any(
        (
            "darwin" in c.PLATFORM_LOWER,
            "macos" in c.PLATFORM_LOWER,
        )
    ):
        if jarpyvscode.insiders.is_insiders():
            vscode_search_string_lw = "visual studio code - insiders.app"
        else:
            vscode_search_string_lw = "visual studio code"
    elif "windows" in c.PLATFORM_LOWER:
        vscode_search_string_lw = "Code.exe"
        logger.warning("psutil has a bug that must be fixed!")
    elif "linux" in c.PLATFORM_LOWER:
        if jarpyvscode.insiders.is_insiders():
            vscode_search_string_lw = "/code-insiders"
        else:
            vscode_search_string_lw = "/code"

    cmd = ["ps", "-A", "-o", "command"]
    stdout, stderr = "", ""
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True)
    if p.stdout:
        for line in p.stdout:
            if vscode_search_string_lw in line.lower() and not any(
                (
                    # Ignore process
                    # - which runs this Python VS Code API
                    # - crashpad handler which keeps running, when quitting VS Code
                    re.findall(r"vscode.*?launch", line.lower()),
                    re.findall(r"chrome_crashpad_handler", line.lower()),
                )
            ):
                stdout += line
    if p.stderr:
        for _, line in enumerate(p.stderr):
            stderr += line
    while p.poll() is None:
        pass
    if stdout:
        logger.debug("Identified that VSCode is alive.")
        if print_to_stdout:
            print(1)
        return True
    logger.debug("Identified that VSCode is NOT alive.")
    if print_to_stdout:
        print(0)
    return False

    # try:
    #     for proc in psutil.process_iter(attrs=('pid', 'exe',)):
    #         try:
    #             exe = proc.info['exe']
    #         except (psutil.AccessDenied, psutil.NoSuchProcess):
    #             exe = None
    #         if exe is not None and vscode_exe_name_lw in exe.lower():
    #             print(1)
    #             return True
    #     print(0)
    # except FileNotFoundError as e:
    #     error(str(e))
    # return False


def collect_vsc_config_file_paths() -> t.List[str]:
    """Collect paths for existing config files to be adapted.

    This includes paths to the following types of files:

    * ``Code/User/settings.json``
    * ``Code/storage.json``
    * ``.code-workspace`` files from
      ``User/globalStorage/jamilraichouni.jarpyvscode/workspaces``
    * ``.env`` and ``tasks.json`` file s for workspaces
    * ``state.vscdb``
    * ``state.vscdb.backup``
    * ``workspace.json``

    Returns
    -------
    t.List[str]
        List of absolute paths for existing config files

    """
    file_paths = []

    # settings.json and storage.json in dir 'appdata':
    settings_file_path = jarpyvscode.paths.normalise_path(
        str(jarpyvscode.paths.user_settings_path())
    )
    if isfile(settings_file_path):
        file_paths.append(settings_file_path)

    storage_file_path = jarpyvscode.paths.normalise_path(
        join(
            str(jarpyvscode.paths.code_dir()),
            "storage.json",
        )
    )
    if isfile(storage_file_path):
        file_paths.append(storage_file_path)

    # .code-workspace files:
    workspace_cfgs_dir: Path = jarpyvscode.paths.workspace_cfgs_dir()
    if workspace_cfgs_dir.is_dir():
        workspace_def_file_paths: t.List[str] = [
            join(str(jarpyvscode.paths.workspace_cfgs_dir()), n)
            for n in os.listdir(str(jarpyvscode.paths.workspace_cfgs_dir()))
            if n.endswith(".code-workspace")
        ]
        workspace_def_file_paths = list(
            map(jarpyvscode.paths.normalise_path, workspace_def_file_paths)
        )
        file_paths += workspace_def_file_paths
        file_paths += workspace_specific_file_paths(
            workspace_def_file_paths=workspace_def_file_paths
        )

    for storage_name in ("globalStorage", "workspaceStorage"):
        storage_dir_path = join(str(jarpyvscode.paths.user_dir()), storage_name)
        for dir_path, _, file_names in os.walk(storage_dir_path):
            to_adapt_names = ("state.vscdb", "state.vscdb.backup", "workspace.json")
            for file_name in [f for f in file_names if f in to_adapt_names]:
                file_path = jarpyvscode.paths.normalise_path(join(dir_path, file_name))
                file_paths.append(file_path)
    file_paths = sorted(file_paths)
    return file_paths


def find_python_packages(first_root_folder_path: Path) -> t.List[str]:
    """Find folders containing a ``__init__.py`` file.

    Returns
    -------
    t.List[str]
        List of sub folder names

    """
    python_package_names: t.List[str] = []
    child: Path
    for child in first_root_folder_path.iterdir():
        if child.is_dir():
            init_py_file_path = child.joinpath("__init__.py")
            if init_py_file_path.exists():
                python_package_names.append(child.name)
    return sorted(python_package_names)


def find_sphinx_config_file(
    project_path: Path, settings: t.Dict[str, t.Any]
) -> t.Optional[Path]:
    """Find Sphinx configuration file.

    Check if the setting ``"restructuredtext.confPath"`` is given in *settings* and use
    its value if it points to an existing directory containing a ``conf.py`` file.

    If the setting is not given or is not pointing to an existing directory containing a
    ``conf.py`` file, this function recursively searches through the directory specified
    via *project_path*.

    To increase the speed the recursive search will ignore the following subfolders:

    * ``.git/``
    * ``.svn/``
    * ``.venv/``
    * ``.vscode/``
    * ``conda_env/``
    * ``conda_envs/``
    * ``docs/build/``
    * ``env/``
    * ``envs/``
    * ``venv/``
    * ``venvs/``

    Parameters
    ----------
    project_path
        Path to the first root folder of the workspace

    settings
        Settings read from ``.vscode/settings.json`` for the first root folder

    Returns
    -------
    t.Optional[Path]
        Path to the Sphinx configuration file named ``conf.py``.

    """
    conf_py_file_path: t.Optional[Path] = None
    key: str = "restructuredtext.confPath"
    is_conf_py_file_found: bool = False
    if key in settings:
        conf_py_file_path = Path(settings[key]) / "conf.py"
        if conf_py_file_path.is_file():
            return conf_py_file_path
    conf_py_file_path = None
    to_ignore_dirs = (
        project_path / ".git",
        project_path / ".svn",
        project_path / ".venv",
        project_path / ".vscode",
        project_path / "conda_env",
        project_path / "conda_envs",
        project_path / "docs" / "build",
        project_path / "env",
        project_path / "envs",
        project_path / "venv",
        project_path / "venvs",
    )
    for dir_path, _, file_names in os.walk(top=project_path):
        is_ignore_dir: bool = False
        for to_ignore_dir in to_ignore_dirs:
            is_ignore_dir = dir_path == str(to_ignore_dir) or dir_path.startswith(
                str(to_ignore_dir)
            )
            if is_ignore_dir:
                break
        if is_ignore_dir:
            continue
        file_name: str
        for file_name in file_names:
            file_path: str = join(dir_path, file_name)
            is_conf_py_file_found = all(
                (file_name == "conf.py", Path(Path(dir_path) / "index.rst").is_file())
            )
            if is_conf_py_file_found:
                conf_py_file_path = Path(file_path)
                if dir_path == str(project_path / "docs" / "source"):
                    break
        if is_conf_py_file_found:
            break
    return conf_py_file_path


def workspace_specific_file_paths(workspace_def_file_paths: t.List[str]):
    """Return ``.env`` and ``tasks.json`` file paths for workspaces.

    Read ``path`` values for workspace folders defined in
    ``.code-workspace`` files and check for ``.env`` and ``tasks.json``
    files in the workspace.

    Parameters
    ----------
    workspace_def_file_paths
        List of Paths to ``.code-workspace`` files containing workspace
        configurations

    Returns
    -------
    list
        File paths to ``.env`` and ``tasks.json`` files in workspaces

    """
    file_paths: t.List[str] = []
    for workspace_def_file_path in workspace_def_file_paths:
        with open(workspace_def_file_path, "r") as f:
            try:
                workspace_def_json = json.load(f, object_pairs_hook=OrderedDict)
            # There is a json.JSONDecodeError but no json.JSONDecodeError.
            # Hence, BaseException is being catched here:
            except BaseException as e:
                print(
                    f'json.load() on file "{workspace_def_file_path}" '
                    f"raised exception: {str(e)}"
                )
                continue
        for folder in workspace_def_json["folders"]:
            workspace_dir_path = jarpyvscode.paths.normalise_path(folder["path"])
            workspace_dir_path = adapt_jarroot_in_path(old_path=workspace_dir_path)
            if not isdir(workspace_dir_path):
                continue

            # .env files:
            env_file_paths: t.List[str] = [
                join(workspace_dir_path, f)
                for f in os.listdir(workspace_dir_path)
                if f.lower().endswith(".env")
            ]
            env_file_paths = list(map(jarpyvscode.paths.normalise_path, env_file_paths))
            file_paths += env_file_paths

            # tasks.json files:
            tasks_file_path = jarpyvscode.paths.normalise_path(
                join(workspace_dir_path, ".vscode", "tasks.json")
            )
            if isfile(tasks_file_path):
                file_paths.append(tasks_file_path)
    file_paths = list(map(jarpyvscode.paths.normalise_path, file_paths))
    file_paths = sorted(list(set(file_paths)))  # makes entries unique and sort
    return file_paths
