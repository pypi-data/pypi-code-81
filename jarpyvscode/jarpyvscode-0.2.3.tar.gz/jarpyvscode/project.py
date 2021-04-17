"""Module with tools to deal with VSCode projects."""

# Standard library:
import os
import re
import typing as t
from pathlib import Path

# 3rd party:
from cookiecutter.main import cookiecutter

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.projects.pythonproject
import jarpyvscode.projects.vsce
import jarpyvscode.usersettings
from jarpyvscode.log import logger
from jarpyvscode.projects.baseproject import BaseProject

VALID_REPO_NAME_PATTERN: str = r"^[a-zA-Z0-9-_\.]+$"


def compute_path(name_or_path: str) -> t.Optional[Path]:
    r"""Compute path based on value for project name/ path providing by VSCode user.

    The Visual Studio Code extension command ``"jarpyvscode.createProject"`` open a text
    input field to enter a project name/ path.

    This function determines, if the user entered something that is path-like (contains
    a ``"/"`` or ``"\"``. If that is true, the function checks if the desired parent
    directory exists and if so, if a project with the provided name is already given in
    that parent directory.

    If the user just entered a project name, this function will check, if the project
    name is valid (e. g. does not contain a blank).

    An error will be logged if the desired project name is not valid.

    When the user provided a valid project name, the parent directory will be read from
    the extension's setting ``"jarpyvscode.cookiecutter.projects.outputPath"`` and will
    log an error, if that output directory does not exist of when the user has no
    permissions to write into that directory.

    If ``"jarpyvscode.cookiecutter.projects.outputPath"`` is not configured and a valid
    project name has been passed, the project will be created in the users's home
    directory.

    Parameters
    ----------
    name_or_path
        String provided by the user for the project path/ name

    Returns
    -------
    t.Optional[Path]
        Path

    """
    path: t.Optional[Path] = None
    is_potential_path: bool = "/" in name_or_path or "\\" in name_or_path
    if is_potential_path:
        logger.debug(f"User provided a potential full project path '{name_or_path}'.")
        path = Path(name_or_path)
        if not is_output_path_valid(output_path=path.parent, project_name=path.name):
            return None
    else:
        logger.debug(f"User provided a potential project name '{name_or_path}'.")
        output_path: str = str(
            jarpyvscode.usersettings.read_user_setting(
                "jarpyvscode.cookiecutter.projects.outputPath"
            )
        )
        if output_path == "None" or not output_path:
            output_path = str(Path.home())
            logger.debug(
                "User has not configured "
                "'jarpyvscode.cookiecutter.projects.outputPath'. "
                f"Project parent directory might be '{Path.home()}'."
            )
        if not Path(output_path).is_dir():
            logger.error(
                "The setting 'jarpyvscode.cookiecutter.projects.outputPath' points "
                f"to a not existing directory '{output_path}'!"
            )
            return None
        path = Path(output_path) / name_or_path
        if not is_output_path_valid(
            output_path=Path(output_path), project_name=name_or_path
        ):
            return None
    return path


def create(name_or_path: str, template_kind: str):
    """Create new VSCode project from cookiecutter template and initialise it with Git.

    This function does nothing except logging an information, if *name_or_path* points
    to an existing project directory.

    Parameters
    ----------
    name_or_path
        String provided by the user for the project path/ name
    template_kind
        Kind of the cookiecutter template to create the project from

    """
    logger.debug(
        "Python backend received: "
        f"name_or_path = '{name_or_path}', "
        f"template_kind = '{template_kind}'."
    )
    project_path = compute_path(name_or_path=name_or_path)
    if project_path is None:
        return
    project_name: str = project_path.name
    cc_projects: t.List[t.Any] = list(
        jarpyvscode.usersettings.read_user_setting("jarpyvscode.cookiecutter.projects")  # type: ignore # noqa
    )
    if cc_projects is not None:
        cc_projects = [
            p for p in list(cc_projects) if "kind" in p and p["kind"] == template_kind
        ]
        cc_project: t.Dict[str, t.Union[str, t.Dict[str, str]]] = cc_projects[0]
        uri: str = str(cc_project["uri"])
        if "directory" in cc_project and cc_project["directory"] is not None:
            uri = f"{uri}/{cc_project['directory']}"
        extra_context: t.Dict[str, str] = {"repo_name": project_name}
        if "configuration" in cc_project:
            extra_context = {
                **extra_context,
                **cc_project["configuration"],  # type: ignore
            }
        out_dir: Path = project_path.parent
        try:
            cookiecutter(
                template=uri,
                output_dir=str(out_dir),
                no_input=True,
                extra_context=extra_context,
            )
            setup(project_path=project_path)
        except Exception as e:
            logger.error(f"Creating project from template failed: '{e}'")
            return
    logger.info("DONE.")


def is_output_path_valid(output_path: Path, project_name: str) -> bool:
    """Check if *output_path* and *project_name* are valid.

    Check if the directory *output_path* exists and if the user can write into it.
    When this is given *project_name* will be passed to
    :func:`jarpyvscode.project.is_project_name_valid` to check if the selected name for
    the project is valid. If that is also true it will be checked, if there is already
    a directory *project_name* in the folder *output_path*.

    Parameters
    ----------
    output_path
        Potential parent directory to create a project named *project_name*
    project_name
        Potential project name.

    Returns
    -------
    bool
        True, when *output_path* and *project_name* are valid

    """
    if not output_path.is_dir():
        logger.info(f"The output directory '{output_path}' does not exist!")
        return False
    if not os.access(output_path, os.W_OK):
        logger.info(
            f"Writing into the output directory '{output_path}' is not permitted!"
        )
        return False
    if not is_project_name_valid(name=project_name):
        return False
    if Path(output_path / project_name).exists():
        logger.info(f"'{Path(output_path / project_name)}' already exists!")
        return False
    return True


def is_project_name_valid(name: str) -> bool:
    """Check if a project name is a valid name for a repository.

    A project name must match the pattern ``"^[a-zA-Z0-9-_.]+$"``.

    Parameters
    ----------
    name
        Desired project name as defined by the user

    """
    is_valid: bool = re.match(VALID_REPO_NAME_PATTERN, name) is not None
    if not is_valid:
        logger.warning(
            f"The provided project name '{name}' is not valid. "
            f"The project name must match the pattern '{VALID_REPO_NAME_PATTERN}'."
        )
    return is_valid


def setup(project_path: Path):
    """Set up a VSCode project.

    Parameters
    ----------
    project_path
        Path to the project root directory

    """
    project_path = project_path.resolve()
    if not project_path.is_dir():
        logger.error(f"The directory '{project_path}' does not exist!")
        return
    project_kind: t.Optional[str] = BaseProject(path=project_path).kind
    if project_kind is None:
        return
    project: t.Optional[BaseProject] = None
    if project_kind == c.PROJECT_KIND_PYTHON:
        project = jarpyvscode.projects.pythonproject.Project(path=project_path)
    if project is not None:
        project.setup()
