"""Module defining an abstract class :class:`Project`."""

# Standard library:
import json
import shutil
import subprocess
import typing as t
from pathlib import Path

# 3rd party:
import json5
import toml

# local:
import jarpyvscode.constants as c
import jarpyvscode.jsonutils
import jarpyvscode.paths
import jarpyvscode.strings
import jarpyvscode.usersettings
import jarpyvscode.utils
from jarpyvscode.log import logger


class BaseProject:
    """A class representing a generic VSCode project.

    Specific project classes will be based on this more abstract class that provides
    commonly needed methods.

    """

    def __init__(self, path: Path):
        """Initialise the project.

        Parameters
        ----------
        path
            Absolute path to the root directory of the project

        """
        self._path = path
        self.determine_kind()

    # kind:
    @property
    def kind(self) -> t.Optional[str]:
        """Return kind of project."""
        return self._kind

    # name:
    @property
    def name(self) -> str:
        """Return name of project."""
        return self.path.name

    # path:
    @property
    def path(self) -> Path:
        """Return path of project."""
        return self._path

    @path.setter
    def path(self, path: Path):
        """Set path of project."""
        self._path = path

    def copy_template_file(self, src: Path, dest: Path, **kwargs: str):
        """Copy template file and optionally populate placeholders.

        Parameters
        ----------
        src
            Path to source file

        dest
            Path to destination file

        kwargs
            Key/ value pairs with:

            * key: placeholder name
            * val: value for the placeholder to be filled

        """
        if not src.is_file():
            logger.warning(f'Cannot find template file "{src}"!')
            return
        if not dest.parent.is_dir():
            logger.warning(f'Cannot copy template file "{src}" to {dest}!')
            return
        # copy template file:
        logger.info(f"Create file '{dest.name}' ...")
        shutil.copy2(src, dest)
        if dest.is_file() and kwargs is not None and kwargs:
            populated_content: str = jarpyvscode.strings.fill_placeholders(
                subject=dest.read_text(), **kwargs
            )
            dest.write_text(populated_content)

    def create_workspace_cfg_file(
        self,
    ) -> t.Tuple[t.Dict[str, t.Any], t.Optional[Path]]:
        """Create workspace configuration file if it does not exist.

        Returns
        -------
        t.Tuple[t.Dict[str, t.Any], t.Optional[Path]]
            Tuple with basic workspace configuration as first element and the path to
            a created workspace configuration file when it could be created.

        """
        workspace_defs_dir: Path = Path(
            jarpyvscode.paths.user_dir()
            / ("globalStorage/jamilraichouni.jarpyvscode/workspaces")
        )
        workspace_cfg_file_path: Path = (
            workspace_defs_dir / f"{self.name}.code-workspace"
        )
        logger.info(
            f"Create workspace configuration file '{workspace_cfg_file_path}' ..."
        )
        workspace_cfg: t.Dict[str, t.Any] = {}
        if workspace_cfg_file_path.is_file():
            logger.info(
                f"Workspace configuration '{workspace_cfg_file_path}' already exists."
            )
        workspace_cfg = {
            "folders": [{"name": self.name, "path": str(self.path)}],
            "settings": {
                "git.ignoreLimitWarning": True,
                "restructuredtext.languageServer.disabled": True,
            },
        }
        try:
            workspace_cfg_file_path.write_text(json.dumps(workspace_cfg, indent=4))
        except Exception as e:
            logger.warning(f"Creation of workspace configuration file failed: '{e}'")
            return workspace_cfg, None
        return workspace_cfg, workspace_cfg_file_path

    def determine_kind(self):
        """Determine the kind of the VSCode project."""
        self._kind = None
        python_project_root_file_name: str
        for python_project_root_file_name in c.PYTHON_PROJECT_ROOT_FILE_NAMES:
            if Path(self.path / python_project_root_file_name).is_file():
                self._kind = c.PROJECT_KIND_PYTHON
                break
        if self.kind is None:
            logger.warning(f"Cannot determine the kind for the project '{self.path}'!")

    def initialise_with_git(self):
        """Initialise project directory with Git."""
        if Path(self.path / ".git").is_dir():
            logger.info(
                f"'{self.kind}' project '{self.path}' is already a Git repository."
            )
            return
        cmd: t.List[str] = ["git", "init"]
        try:
            logger.info(f"Initialise '{self.kind}' project '{self.path}' with Git ...")
            subprocess.check_call(cmd, cwd=self.path)
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Initialising '{self.kind}' project '{self.path}' "
                f"with Git failed: {e}"
            )

    def read_configuration(self, filename: str) -> t.Dict[str, t.Any]:
        """Read configuration from ``.vscode/(launch|settings|tasks).json`` file.

        Return empty dictionary if the JSON file does not exist.

        Parameters
        ----------
        filename
            ``"launch.json"``, ``"settings.json"``, or ``"tasks.json"``

        Returns
        -------
        t.Dict[str, t.Any]
            Dictionary with configuration

        Raises
        ------
        ValueError
            If an existing configuration file can not be read (invalid JSON).

        """
        configuration: t.Dict[str, t.Any] = {}
        file_path: Path = self.path / ".vscode" / filename
        if not file_path.is_file():
            return configuration
        try:
            configuration = json5.loads(file_path.read_text())
        except ValueError as e:
            logger.error(f"Cannot parse the file '{file_path}': {str(e)}")
        return configuration

    def setup(self) -> None:
        """Set up VSCode project."""
        logger.info(f"Set up '{self.kind}' VSCode project '{self.path}' ...")
        self.initialise_with_git()
        self.setup_workspace_cfg_file()

    def setup_workspace_cfg_file(self):
        """Set up workspace configuration file ."""
        workspace_defs_dir: Path = Path(
            jarpyvscode.paths.user_dir()
            / "globalStorage/jamilraichouni.jarpyvscode/workspaces"
        )
        workspace_cfg_file_path: t.Optional[Path] = (
            workspace_defs_dir / f"{self.name}.code-workspace"
        )
        if workspace_cfg_file_path.is_file():
            workspace_cfg = json5.loads(workspace_cfg_file_path.read_text())
            logger.info(
                f"Set up workspace configuration file '{workspace_cfg_file_path}' ..."
            )
        else:
            workspace_cfg, workspace_cfg_file_path = self.create_workspace_cfg_file()
        workspace_cfg_file_path_existing: Path
        if Path(str(workspace_cfg_file_path)).is_file():
            workspace_cfg_file_path_existing = Path(str(workspace_cfg_file_path))
        else:
            return
        if workspace_cfg is not None:
            # folders:
            if "folders" in workspace_cfg:
                configured_folder_paths: t.List[str] = []
                [
                    configured_folder_paths.append(f["path"])
                    for f in workspace_cfg["folders"]
                ]
                if str(self.path) not in configured_folder_paths:
                    workspace_cfg["folders"].insert(
                        0, {"name": self.name, "path": str(self.path)}
                    )
            else:
                workspace_cfg["folders"] = [{"name": self.name, "path": str(self.path)}]
            # settings:
            if "settings" in workspace_cfg:
                workspace_cfg["settings"]["git.ignoreLimitWarning"] = True
                workspace_cfg["settings"][
                    "restructuredtext.languageServer.disabled"
                ] = True
            else:
                workspace_cfg["settings"] = {
                    "git.ignoreLimitWarning": True,
                    "restructuredtext.languageServer.disabled": True,
                }
            workspace_cfg_file_path_existing.write_text(
                json.dumps(workspace_cfg, indent=4)
            )

        # adapt JARROOT in all string values:
        workspace_config: str = workspace_cfg_file_path_existing.read_text()

        val: t.Union[Path, str, int, float]
        for val in jarpyvscode.jsonutils.json_values_of_type_generator(
            json_info=workspace_cfg_file_path_existing,
            value_type=str,
        ):
            val = str(val)
            # double backslashs as path separator!
            # any '\\' in the file have been transformed to '\'
            # when the file has been parsed by json but we directly work on the string
            # for the file content, we must consider, that single backslashs that have
            # been read appear as double backslashs in the file content's string.
            sep: str = "\\\\" if "windows" in c.PLATFORM_LOWER else "/"
            new_val: str = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=val, sep=sep
            )
            val = str(val).replace("\\", "\\\\")

            # ensure that new val does not contain single backslashs:
            new_val = new_val.replace("\\\\", "~~|~~")  # store double backslashs
            new_val = new_val.replace(
                "\\", "\\\\"
            )  # replace single by double backslashs
            new_val = new_val.replace("~~|~~", "\\\\")  # restore double backslashs

            workspace_config = workspace_config.replace(f'"{val}"', f'"{new_val}"')
        workspace_cfg_file_path_existing.write_text(workspace_config)

    def write_configuration(
        self, filename: str, configuration: t.Dict[str, t.Any], sort_keys: bool = True
    ):
        """Write configuration to ``.vscode/(launch|settings|tasks).json`` file.

        Parameters
        ----------
        filename
            ``"launch.json"``, ``"settings.json"``, or ``"tasks.json"``

        configuration
            Dictionary with configuration

        sort_keys : optional
            Sort keys in configuration that will be written

        """
        file_path: Path = self.path / ".vscode" / filename
        file_path.write_text(
            json.dumps(configuration, sort_keys=sort_keys, indent=4) + "\n"
        )
