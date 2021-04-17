"""Module with class handling Visual Studio Code Extension projects."""

# Standard library:
import json
import subprocess
import typing as t
from pathlib import Path

# 3rd party:
import json5

# local:
import jarpyvscode.constants as c
from jarpyvscode.log import logger
from jarpyvscode.projects.baseproject import BaseProject

MODULE_DIR: Path = Path(__file__).parents[0]


class Project(BaseProject):
    """A class representing a Visual Studio Code Extension project."""

    def __init__(self, path: Path):
        """Initialise the project.

        Parameters
        ----------
        path
            Absolute path to the root directory of the project

        """
        super().__init__(path=path, kind=c.PROJECT_KIND_VSCE)
        if not self.path.exists():
            self.create()

    def create(self):
        """Create project."""
        if not self.create_vsce_project():
            return
        self.setup()

    def create_vsce_project(self) -> bool:
        """Create Visual Studio Code Extension project via ``yo code``.

        Returns
        -------
        bool
            Success flag that is true, if the method succeeds

        """
        cmd: t.List[str] = [
            "yo",
            "code",
            "--extensionType=command-ts",
            f"--extensionName={self.name}",
            f"--extensionDescription={self.name}",
            f"--extensionDisplayName={self.name}",
            "--pkgManager=npm",
            "--gitInit",
            "--webpack=No",
        ]
        try:
            logger.info(f"Create '{self.kind}' project '{self.path}' ...")
            subprocess.check_call(cmd, cwd=self.path.parent)
        except subprocess.CalledProcessError as e:
            if not self.path.exists():
                logger.error(
                    f"Creating a new Visual Studio Code Extension project failed: {e}"
                )
                return False
        return True

    def setup(self):
        """Set up project."""
        super().setup()
        self.setup_gitignore()
        self.setup_configuration()

        readme_path: Path = Path(self.path / "README.md")
        if not readme_path.is_file():
            readme_path.write_text(f"# {self.name}\n")

    def setup_configuration(self):
        """Set up sub dir ``.vscode/``."""
        self.setup_package_json()
        self.setup_settings()
        self.setup_tasks()

    def setup_gitignore(self):
        """Add ``build`` directory to ``.gitignore`` file."""
        file_path: Path = self.path.joinpath(".gitignore")
        if file_path.is_file():
            logger.info(f"Set up file '{file_path.name}' ...")
        else:
            logger.warning(f"Cannot find file '{file_path}'!")
            return
        file_content: str = file_path.read_text()
        lines: t.List[str] = (
            file_content.split() if "\n" in file_content else [file_content]
        )
        if "build/" not in lines:
            logger.info("Add 'build' directory to '.gitignore' file ...")
            lines.insert(0, "build/")
        file_path.write_text("\n".join(lines) + "\n")

    def setup_package_json(self):
        """Set up ``package.json`` file.

        Set publisher to ``jar``.
        """
        file_path: Path = self.path.joinpath("package.json")
        if file_path.is_file():
            logger.info(f"Set up file '{file_path.name}' ...")
        else:
            logger.error(f"Cannot find file '{file_path}'!")
            return
        configuration: t.Dict[str, t.Any] = json.loads(file_path.read_text())
        logger.info(f"Set publisher to 'jar' in '{file_path.name}' ...")
        configuration["publisher"] = "jar"
        logger.info(f"Set up 'galleryBanner' in '{file_path.name}' ...")
        configuration["galleryBanner"] = {"color": "white", "theme": "dark"}
        repo_url: str = f"https://gitlab.com/jar1/{self.name}.git"
        logger.info(
            f"Set up 'repository' (url: '{repo_url}') in '{file_path.name}' ..."
        )
        configuration["repository"] = {
            "type": "git",
            "url": repo_url,
        }
        file_path.write_text(json.dumps(configuration, sort_keys=True, indent=4) + "\n")

    def setup_settings(self):
        """Set up ``.vscode/settings.json``.

        This function configures more settings by calling:

        * :meth:`setup_settings_testing`

        """
        settings_file_path: Path = self.path / ".vscode" / "settings.json"
        logger.info(f"Set up '{settings_file_path.name}' ...")
        settings: t.Dict[str, t.Any] = self.read_configuration(filename="settings.json")
        self.setup_settings_testing(settings)
        self.write_configuration(filename="settings.json", configuration=settings)

    def setup_settings_testing(self, settings: t.Dict[str, t.Any]):
        """Set up ``"python.testing.*"`` in ``.vscode/settings.json``.

        ``"python.testing.nosetestsEnabled"``:

        If that setting is not given, it will be introduced with a value of ``false``.


        ``"python.testing.promptToConfigure"``:

        If that setting is not given, it will be introduced with a value of ``false``.


        ``"python.testing.pytestEnabled"``:

        If that setting is not given, it will be introduced with a value of ``false``.


        ``"python.testing.unittestEnabled"``:

        If that setting is not given, it will be introduced with a value of ``false``.

        Parameters
        ----------
        settings
            Dictionary with settings read from ``.vscode/settings.json``.

        """
        keys: t.Tuple[str, str, str, str] = (
            "python.testing.nosetestsEnabled",
            "python.testing.promptToConfigure",
            "python.testing.pytestEnabled",
            "python.testing.unittestEnabled",
        )
        for key in [key for key in keys if key not in settings]:
            settings[key] = False
            logger.debug(f"Set '{key}' to '{settings[key]}'.")

    def setup_tasks(self):
        """Set up tasks in the file ``.vscode/tasks.json``."""
        template_tasks_path: Path = MODULE_DIR.joinpath("templates/vsce/tasks.json")
        tasks_path: Path = self.path / ".vscode/tasks.json"
        logger.info(f"Set up '{tasks_path.name}' ...")
        template_tasks: t.Dict[str, t.Any] = json.loads(template_tasks_path.read_text())
        try:
            tasks: t.Dict[str, t.Any] = json.loads(tasks_path.read_text())
        except json.decoder.JSONDecodeError:
            tasks: t.Dict[str, t.Any] = json5.loads(tasks_path.read_text())
        tasks["inputs"] = template_tasks["inputs"]
        new_tasks: t.List[t.Dict[str, t.Any]] = [template_tasks["tasks"][0]]
        task: t.Dict[str, t.Any]
        for task in tasks["tasks"]:
            if "label" not in task or task["label"] != "VSCE":
                new_tasks.append(task)
        tasks["tasks"] = new_tasks
        tasks_path.write_text(json.dumps(tasks, sort_keys=False, indent=4) + "\n")
