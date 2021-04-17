"""Module with class handling Python (poetry) VSCode projects."""

# Standard library:
import fileinput
import os
import subprocess
import sys
import typing as t
from pathlib import Path

# 3rd party:
import toml

# local:
import jarpyvscode.constants as c
import jarpyvscode.jsonutils
import jarpyvscode.paths
import jarpyvscode.usersettings
import jarpyvscode.utils
import jarpyvscode.venvs
from jarpyvscode.log import logger
from jarpyvscode.projects.baseproject import BaseProject


class Project(BaseProject):
    """A class representing a Python (poetry) VSCode project."""

    def __init__(self, path: Path):
        """Initialise the project.

        Parameters
        ----------
        path
            Absolute path to the root directory of the project

        """
        super().__init__(path=path)
        self.determine_venv_path()

    # venv_path:
    @property
    def venv_path(self) -> t.Optional[Path]:
        """Return class property ``venv_path``."""
        return self._venv_path

    # def create_virtual_environment(self) -> bool:
    #     """Create the virtual environment.

    #     Returns
    #     -------
    #     bool
    #         Success flag that is true, if the method succeeds

    #     """
    #     cmd: t.List[str] = ["poetry", "install", "--no-interaction"]
    #     Path(self.path / "poetry.lock").unlink(missing_ok=True)
    #     time.sleep(2)
    #     try:
    #         logger.info(f"Create virtual environment for project '{self.path}' ...")
    #         subprocess.check_call(
    #             cmd, cwd=self.path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    #         )
    #     except subprocess.CalledProcessError as e:
    #         logger.error(
    #             f"Creating virtual environment for project '{self.path}' failed: {e}"
    #         )
    #         return False
    #     return True

    def determine_venv_path(self):
        """Determine path to virtual environment."""
        self._venv_path: t.Optional[Path] = None
        self.determine_venv_path_pipenv()
        if self.venv_path is None:
            self.determine_venv_path_poetry()
        if self.venv_path is None:
            self.determine_venv_path_builtin_venv()
        if self.venv_path is None:
            logger.warning(
                "Could not identify path to virtual environment for the project "
                f"'{self.path}'!"
            )

    def determine_venv_path_builtin_venv(self):
        """Determine path to ``venv`` (builtin Python) virtual environment."""
        venvs_path_str: str = str(
            jarpyvscode.usersettings.read_user_setting("python.venvPath")
        )
        if Path(venvs_path_str).is_dir():
            venv_path: Path = Path(Path(venvs_path_str) / self.name)
            if venv_path.is_dir():
                self._venv_path = venv_path
                logger.info(f"Identified virtual environment at '{self.venv_path}'.")

    def determine_venv_path_pipenv(self):
        """Determine path to ``venv`` (pipenv) virtual environment."""
        if not any(
            (
                Path(self.path / "Pipfile").is_file(),
                Path(self.path / "Pipfile.lock").is_file(),
            )
        ):
            return
        cmd: t.List[str] = ["pipenv"]
        try:
            subprocess.check_call(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            logger.info("Cannot run the command 'pipenv'!")
            return
        except subprocess.CalledProcessError:
            logger.info("Cannot run the command 'pipenv'!")
            return
        try:
            self._venv_path = Path(
                subprocess.check_output(args=cmd + ["--venv"], cwd=self.path)
                .decode("utf8")
                .replace("\n", "")
                .replace("\r", "")
            )
            logger.info(
                f"Identified virtual environment (pipenv) at '{self.venv_path}'."
            )
        except subprocess.CalledProcessError as e:
            logger.info("Cannot find pipenv virtual environment.")
            logger.debug(f"The command 'pipenv --venv' raised: '{e}'.")
            return

    def determine_venv_path_poetry(self):
        """Determine path to Poetry virtual environment."""
        if not any(
            (
                Path(self.path / "pyproject.toml").is_file(),
                Path(self.path / "poetry.lock").is_file(),
            )
        ):
            return
        cmd: t.List[str]
        if "windows" in c.PLATFORM_LOWER:
            cmd = ["python", f"{os.getenv('USERPROFILE')}\\.poetry\\bin\\poetry"]
        else:
            cmd = ["poetry"]
        try:
            subprocess.check_call(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            logger.info("Cannot run the command 'poetry'!")
            return
        except subprocess.CalledProcessError:
            logger.info("Cannot run the command 'poetry'!")
            return
        try:
            self._venv_path = Path(
                subprocess.check_output(
                    args=cmd + ["env", "info", "--path"], cwd=self.path
                )
                .decode("utf8")
                .replace("\n", "")
                .replace("\r", "")
            )
            logger.info(
                f"Identified virtual environment (poetry) at '{self.venv_path}'."
            )
        except subprocess.CalledProcessError as e:
            logger.info("Cannot find Poetry virtual environment.")
            logger.debug(f"The command 'poetry env info --path' raised: '{e}'.")
            return

    def read_max_line_length_from_pyproject_toml(self) -> int:
        """Try to read line-length cfg for black in pyproject.toml.

        Return default value of 88 if no configuration can be found.

        """
        max_line_length: int = 88
        pyproject_file_path: Path = self.path / "pyproject.toml"
        pyproject_code: str = pyproject_file_path.read_text()
        pyproject_data: t.MutableMapping[str, t.Any] = toml.loads(pyproject_code)
        try:
            max_line_length = pyproject_data["tool"]["black"]["line-length"]
        except KeyError:
            logger.info(
                "Configure maximum line length default of 88 since "
                f"no value has been configured for black in '{pyproject_file_path}' ..."
            )
        return max_line_length

    def setup(self):
        """Set up project."""
        super().setup()
        readme_path: Path = Path(self.path / "README.md")
        if not readme_path.is_file():
            readme_path.write_text(f"# `{self.name}`\n")
        self.setup_environment_variables_definition_file()
        self.setup_settings()

    def setup_environment_variables_definition_file(self):
        r"""Ensure that there is a ``.env`` file in the project.

        If the file does not exist it will be created and contains

        **Example for macOS/ Linux:**

        .. code-block:: text

            DEBUG=0
            PYTHONPATH=/PATH/TO/<FIRST_ROOT_FOLDER>

        If the file exists, the path separator characters (``"/"`` or ``"\\"``) and path
        split characters (``":"`` or ``";"``) will be set depending on the operating
        system in use.

        """
        env_file_path: Path = self.path / ".env"
        if not env_file_path.is_file():
            env_file_content: str = f"DEBUG=0\nPYTHONPATH={self.path}"
            env_file_path.write_text(env_file_content)
        else:
            to_replace_seps: t.Tuple[t.Tuple[str, str], t.Tuple[str, str]]
            if "windows" in c.PLATFORM_LOWER:
                to_replace_seps = (
                    (":", ";"),
                    ("/", "\\"),
                )
            else:
                to_replace_seps = (
                    (";", ":"),
                    ("\\", "/"),
                )
            line: str
            path: str
            for line in fileinput.input(env_file_path, inplace=True):  # type: ignore
                if line.startswith("PYTHONPATH="):
                    # if "env:PYTHONPATH" not in line:
                    #     line = f"PYTHONPATH={self.path}\n"
                    # else:
                    line = line.replace("env:", "~~|~~")
                    # line = line.replace(to_replace_seps[0][0], to_replace_seps[0][1])
                    line = line.replace("~~|~~", "env:")
                    path = line.replace("PYTHONPATH=", "").replace("\n", "")
                    path = jarpyvscode.utils.adapt_jarroot_in_path(
                        old_path=path, sep=to_replace_seps[1][1]
                    )
                    line = f"PYTHONPATH={path}\n"
                    line = line.replace(to_replace_seps[1][0], to_replace_seps[1][1])
                sys.stdout.write(line)
            fileinput.close()

    def setup_settings(self):
        """Set up ``.vscode/settings.json``.

        The following settings will be copied from the global user ``settings.json``
        file if they have not already been configured for the project:

        * ``"editor.rulers"`` will be set to the value configured in the file
          ``pyproject.toml`` or 88 (the default value of ``black``).

        * ``"jupyter.debugJustMyCode"``

        ``"python.envFile"`` will always be set.

        ``"python.analysis.stubPath"`` will always be set to ``"typings"``.

        ``"restructuredtext.confPath"`` will be set if a ``conf.py`` Sphinx
        configuration file can be found parallel to a `ìndex.rst`` file.

        ``"restructuredtext.languageServer.disabled"`` will be set to true since the
        Python package dependency ``snooty`` is not mature and installs ``typing`` even
        into Python with versions > 3.7. That makes it impossible to install ``black``.

        ``"scm.alwaysShowRepositories"`` will be set to false.

        This function configures more settings by calling:

        * :meth:`setup_setting_python_analysis_extraPaths`
        * :meth:`setup_settings_testing`
        * :meth:`setup_settings_tool_paths`

        """
        settings_file_path: Path = self.path / ".vscode" / "settings.json"
        logger.info(f"Set up '{settings_file_path.name}' ...")
        settings: t.Dict[str, t.Any] = self.read_configuration(filename="settings.json")
        user_settings: t.Dict[
            str, t.Any
        ] = jarpyvscode.usersettings.read_user_settings()
        key: str = "editor.rulers"
        settings[key] = [self.read_max_line_length_from_pyproject_toml()]

        key: str = "jupyter.debugJustMyCode"
        if key not in settings and key in user_settings:
            settings[key] = user_settings[key]
            logger.debug(f"\tSet '{key}' to {user_settings[key]}.")

        key = "python.analysis.stubPath"
        settings[key] = "typings"

        key = "python.envFile"
        settings[key] = str(self.path / ".env")

        key = "restructuredtext.confPath"
        conf_py_file_path: t.Optional[Path] = jarpyvscode.utils.find_sphinx_config_file(
            project_path=self.path, settings=settings
        )
        if conf_py_file_path is None:
            if key in settings:
                del settings[key]
        else:
            settings[key] = str(conf_py_file_path.parent)

        key = "restructuredtext.languageServer.disabled"
        settings[key] = True

        key = "scm.alwaysShowRepositories"
        settings[key] = False

        self.setup_setting_python_analysis_extraPaths(settings)
        self.setup_settings_testing(settings)
        self.setup_settings_tool_paths(settings)

        self.write_configuration(filename="settings.json", configuration=settings)

        self.setup_settings_adapt_jarroot_in_string_values(settings_file_path)

    def setup_settings_adapt_jarroot_in_string_values(self, settings_file_path: Path):
        """Adapt ``JARROOT`` for all string values in ``.vscode/settings.json``.

        Parameters
        ----------
        settings_file_path
            Path to the file ``.vscode/settings.json`` for the project

        """
        settings_str: str = settings_file_path.read_text()
        logger.debug(
            f"Adapt 'JARROOT' in string values of '{settings_file_path.name}' ..."
        )
        val: t.Union[Path, str, int, float]
        for val in jarpyvscode.jsonutils.json_values_of_type_generator(
            json_info=settings_file_path,
            value_type=str,
        ):
            val = str(val)
            # double backslashs as path separator!
            # any double backslash in the file have been transformed to single
            # backslashs when the file has been parsed by json but since we directly
            # work on the string for the file content, we also must consider, that
            # single backslashs that have been read appear as double backslashs in the
            # file content's string.
            sep: str = "\\\\" if "windows" in c.PLATFORM_LOWER else "/"
            new_val: str = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=val, sep=sep
            )
            val = val.replace("\\", "\\\\")

            # ensure that new val does not contain single backslashs:
            new_val = new_val.replace("\\\\", "~~|~~")  # store double backslashs
            new_val = new_val.replace(
                "\\", "\\\\"
            )  # replace single by double backslashs
            new_val = new_val.replace("~~|~~", "\\\\")  # restore double backslashs

            settings_str = settings_str.replace(f'"{val}"', f'"{new_val}"')
        settings_file_path.write_text(settings_str)

    def setup_setting_python_analysis_extraPaths(self, settings: t.Dict[str, t.Any]):
        """Set up ``"python.analysis.extraPaths"`` in ``.vscode/settings.json``.

        Parameters
        ----------
        settings
            Dictionary with settings read from ``.vscode/settings.json``.

        """
        key: str = "python.analysis.extraPaths"
        # project dir:
        python_analysis_extra_paths: t.List[Path] = [self.path]
        # site-packages of venv:
        if self.venv_path is not None:
            site_pkgs_path: Path
            if "windows" in c.PLATFORM_LOWER:
                site_pkgs_path = self.venv_path / "Lib" / "site-packages"
            else:
                site_pkgs_path = (
                    list(Path(self.venv_path / "lib").glob("*"))[0] / "site-packages"
                )
            if site_pkgs_path.is_dir():
                python_analysis_extra_paths.append(site_pkgs_path)
        # # identified Python pkgs in project:
        # python_pkg_names: t.List[str] = vscode.utils.find_python_packages(self.path)
        # for python_pkg_name in python_pkg_names:
        #     python_analysis_extra_paths.append(self.path / python_pkg_name)
        if key in settings:
            for python_analysis_extra_path in python_analysis_extra_paths:
                if str(python_analysis_extra_path).lower() not in settings[key]:
                    settings[key].append(python_analysis_extra_path)
            settings[key] = sorted([str(s) for s in settings[key]])
        else:
            settings[key] = sorted([str(s) for s in python_analysis_extra_paths])
        settings[key] = [
            p for p in sorted(list(set(settings[key]))) if Path(p).is_dir()
        ]
        logger.debug("Set the following paths into 'python.analysis.extraPaths':")
        [logger.debug(f"\t'{p}'") for p in settings[key]]

    def setup_settings_testing(self, settings: t.Dict[str, t.Any]):
        """Set up ``"python.testing.*"`` in ``.vscode/settings.json``.

        ``"python.testing.nosetestsEnabled"``:

        If that setting is not given, it will be introduced with a value of ``false``.


        ``"python.testing.promptToConfigure"``:

        If that setting is not given, it will be introduced with a value of ``false``.


        ``"python.testing.pytestEnabled"``:

        If that setting is not given, it will be introduced with a value of ``true``.


        ``"python.testing.unittestEnabled"``:

        If that setting is not given, it will be introduced with a value of ``false``.

        Parameters
        ----------
        settings
            Dictionary with settings read from ``.vscode/settings.json``.

        """
        key: str = "python.testing.pytestEnabled"
        if key not in settings:
            settings[key] = True
            logger.debug(f"Set '{key}' to '{settings[key]}'.")
        keys: t.Tuple[str, str, str] = (
            "python.testing.nosetestsEnabled",
            "python.testing.promptToConfigure",
            "python.testing.unittestEnabled",
        )
        for key in [key for key in keys if key not in settings]:
            settings[key] = False
            logger.debug(f"Set '{key}' to '{settings[key]}'.")

    def setup_settings_tool_paths(self, settings: t.Dict[str, t.Any]):
        """Set up Python development tool paths in ``.vscode/settings.json``.

        The following settings will be set, if a virtual environment for the project is
        known:

        * ``"python.formatting.blackPath"``
        * ``"python.linting.flake8Path"``
        * ``"python.linting.mypyPath"``
        * ``"python.linting.pydocstylePath"``
        * ``"python.linting.vulturePath"``
        * ``"python.pythonPath"``
        * ``"python.sortImports.path"``
        * ``"python.testing.pytestPath"``
        * ``"restructuredtext.linter.executablePath"``

        Parameters
        ----------
        settings
            Dictionary with settings read from ``.vscode/settings.json``.

        """
        logger.info("Set up Python development tool paths in 'settings.json' ...")
        if self.venv_path is None or not self.venv_path.is_dir():
            return
        tools_keys_names: t.Dict[str, str] = {
            "python.formatting.blackPath": "black",
            "python.linting.flake8Path": "flake8",
            "python.linting.mypyPath": "mypy",
            "python.linting.pydocstylePath": "pydocstyle",
            "python.linting.vulturePath": "vulture",
            "python.pythonPath": "python",
            "python.sortImports.path": "isort",
            "python.testing.pytestPath": "pytest",
            "restructuredtext.linter.executablePath": "doc8",
        }
        sub_dir_name: str = "Scripts" if "windows" in c.PLATFORM_LOWER else "bin"
        tool_name: str
        for key, tool_name in tools_keys_names.items():
            tool_path_str: str = (
                f"{self.venv_path}{os.sep}{sub_dir_name}{os.sep}{tool_name}"
            )
            if "windows" in c.PLATFORM_LOWER:
                tool_path_str += ".exe"
            tool_path: Path = Path(tool_path_str)
            if tool_path.exists():
                settings[key] = str(tool_path)
                logger.debug(f"Set '{key}' to '{settings[key]}'.")
            elif key in settings:
                del settings[key]
