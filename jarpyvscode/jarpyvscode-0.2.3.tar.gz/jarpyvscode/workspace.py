"""Module with tools to deal with a workspace in VSCode.

Workspaces are defined in ``.code-workspace`` files.

"""

# Standard library:
import json
import os.path
import typing as t
from pathlib import Path

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.jsonutils
import jarpyvscode.paths
import jarpyvscode.project
import jarpyvscode.usersettings
import jarpyvscode.utils
import jarpyvscode.venvs
from jarpyvscode.log import logger


def read_code_workspace_file(
    code_workspace_file_path: Path,
) -> t.Optional[t.Dict[str, t.Any]]:
    """Read a specified ``.code-workspace`` configuration file.

    Parameters
    ----------
    code_workspace_file_path
        Absolute path to a ``.code-workspace`` configuration file

    Returns
    -------
    t.Optional[t.Dict[str, t.Any]]
        Dictionary with workspace configuration data read from the ``.code-workspace``
        configuration file or None, if the file cannot be parsed

    Raises
    ------
    ValueError
        If the ``.code-workspace`` configuration file could not be parsed (JSON).

    """
    config: t.Optional[t.Dict[str, t.Any]] = None
    config_str: str = code_workspace_file_path.read_text(encoding="utf8")
    try:
        config = json.loads(config_str)
    except ValueError as e:
        logger.error(f"Cannot parse the file '{code_workspace_file_path}': {str(e)}")
        raise e
    return config


def setup(code_workspace_file_path: Path) -> None:
    """Set up a workspace starting with the ``.code-workspace`` configuration file.

    This function adapts ``JARROOT`` in all string values and calls the following
    functions:

    * :func:`read_code_workspace_file`
    * :func:`setup_folders`
    * :func:`jarpyvscode.project.setup`

    Parameters
    ----------
    code_workspace_file_path
        Path to a ``.code-workspace`` file

    Raises
    ------
    FileNotFoundError
        If the file *code_workspace_file_path* does not exist.

    """
    # todo: Ensure that the list of called functions in the docstring is complete
    logger.info("Set up workspace ...")

    if not code_workspace_file_path.is_file():
        raise FileNotFoundError(code_workspace_file_path)

    config: t.Optional[t.Dict[str, t.Any]] = read_code_workspace_file(
        code_workspace_file_path
    )
    if config is None:
        return

    # folders:
    first_root_folder_path: t.Optional[Path]
    config, first_root_folder_path = setup_folders(
        config=config,
        code_workspace_file_path=code_workspace_file_path,
    )

    # write workspace configuration file:
    code_workspace_file_path.write_text(
        json.dumps(obj=config, indent=4, sort_keys=True)
    )

    # adapt JARROOT in all string values:
    workspace_config_str: str = code_workspace_file_path.read_text()

    val: t.Union[Path, str, int, float]
    for val in jarpyvscode.jsonutils.json_values_of_type_generator(
        json_info=code_workspace_file_path,
        value_type=str,
    ):
        val = str(val)
        # double backslashs as path separator!
        # any double backslash in the file have been transformed to single backslashs
        # when the file has been parsed by json but since we directly work on the string
        # for the file content, we also must consider, that single backslashs that have
        # been read appear as double backslashs in the file content's string.
        sep: str = "\\\\" if "windows" in c.PLATFORM_LOWER else "/"
        new_val: str = jarpyvscode.utils.adapt_jarroot_in_path(old_path=val, sep=sep)
        val = val.replace("\\", "\\\\")

        # ensure that new val does not contain single backslashs:
        new_val = new_val.replace("\\\\", "~~|~~")  # store double backslashs
        new_val = new_val.replace("\\", "\\\\")  # replace single by double backslashs
        new_val = new_val.replace("~~|~~", "\\\\")  # restore double backslashs

        workspace_config_str = workspace_config_str.replace(f'"{val}"', f'"{new_val}"')
    code_workspace_file_path.write_text(workspace_config_str)

    # Configuration and content for root folder of the workspace:
    if first_root_folder_path is None:
        logger.warning(
            f"Workspace configuration '{code_workspace_file_path}' "
            "does not list any folder!"
        )
        # try if we can find a project according to the workspace cfg file name:
        jarroot = Path(str(jarpyvscode.usersettings.jarroot()))
        if jarroot.is_dir():
            project_path: Path = jarroot / "repos" / code_workspace_file_path.stem
            if project_path.is_dir():
                jarpyvscode.project.setup(project_path=project_path)
    elif first_root_folder_path.is_dir():
        jarpyvscode.project.setup(project_path=first_root_folder_path)


def setup_folders(
    config: t.Dict[str, t.Any],
    code_workspace_file_path: Path,
) -> t.Tuple[t.Dict[str, t.Any], t.Optional[Path]]:
    r"""Set up folder paths in data read from ``.code-workspace`` configuration file.

    Iterate over all folder definitions and perform the following actions:

    * Make relative paths absolute,
    * adapt the path according to the definition for ``JARROOT`` on the used development
      computer,
    * remove the folder if it contains a path definition pointing to a directory that
      does not exist,
    * if not given and not already used by another folder entry: introduce a
      ``"name"`` for the folder and set it to the base name of the directory read from
      the attribute path, and
    * set the character separating path components according to the current operating
      system (``"\\"`` for Windows, ``"/"`` for other systems).

    Parameters
    ----------
    config
        Dictionary with workspace configuration data
    code_workspace_file_path
        Absolute path to a ``.code-workspace`` configuration file

    Returns
    -------
    t.Tuple[t.Dict[str, t.Any], t.Optional[Path]]

        * Item 0: Dictionary with potentially updated workspace configuration data.
        * Item 1: Optional path of the first root folder entry in the workspace
                  configuration file or None

    """
    if "folders" not in config:
        logger.warning(
            f"The workspace configuration file '{code_workspace_file_path}' "
            "does not contain any folders."
        )
        return (config, None)
    logger.info(f"Set up folders in '{code_workspace_file_path}' ...")
    folders: t.List[t.Dict[str, str]] = config["folders"]
    workspace_def_files_dir: Path = Path(code_workspace_file_path).parent
    valid_folders: t.List[t.Dict[str, str]] = []
    folder: t.Dict[str, str]
    for folder in folders:
        old_dir_path = Path(folder["path"])
        if (
            Path(
                os.path.abspath(str(Path(workspace_def_files_dir / old_dir_path)))
            ).is_dir()
            and not old_dir_path.is_absolute()
        ):
            # Path().resolve() does not work here since it resolves symlinks.
            # /Users/jamilraichouni/Library/Application Support/Code - Insiders is a
            # symlink pointing to /Users/jamilraichouni/repos/Code.
            # Therefore, the following
            # PosixPath(
            #     "/Users/jamilraichouni/Library/Application Support/"
            #     "Code - Insiders/User/globalStorage/jamilraichouni.jarpyvscode/"
            #     "workspaces/../../../../../../../repos/jar'
            # )
            # is resolved to
            # PosixPath('/Users/repos/jar')
            # which is wrong. Correct is: PosixPath('/Users/jamilraichouni/repos/jar')
            old_dir_path = Path(
                os.path.abspath(str(Path(workspace_def_files_dir / old_dir_path)))
            )
        new_dir_path: Path
        if old_dir_path.resolve().is_dir():
            new_dir_path = old_dir_path
        else:
            new_dir_path = Path(
                jarpyvscode.utils.adapt_jarroot_in_path(old_path=old_dir_path, sep="/")
            )
            new_dir_path = Path(jarpyvscode.paths.normalise_path(new_dir_path))
            if "windows" in c.PLATFORM_LOWER:  # pragma: no cover
                new_dir_path = Path(jarpyvscode.paths.path_backslashed(new_dir_path))
            else:
                new_dir_path = Path(
                    jarpyvscode.paths.path_remove_drive_letter(new_dir_path)
                )
            old_dir_path = Path(folder["path"])
        if new_dir_path.resolve().is_dir():
            if old_dir_path != new_dir_path:
                logger.debug(f"Replace path '{old_dir_path}' by '{new_dir_path}' ...")
            folder["path"] = str(new_dir_path)
            folder["name"] = Path(folder["path"]).name
            if folder not in valid_folders:
                valid_folders.append(folder)
        else:
            logger.warning(
                f"Folder with invalid path '{new_dir_path}' removed from "
                f"'{code_workspace_file_path}'."
            )
    config["folders"] = valid_folders
    first_root_folder_path: t.Optional[Path] = None
    if config["folders"]:
        folder_no: int
        for folder_no, folder in enumerate(config["folders"]):
            if "path" in folder:
                if not folder_no:
                    first_root_folder_path = Path(folder["path"])
    return (config, first_root_folder_path)
