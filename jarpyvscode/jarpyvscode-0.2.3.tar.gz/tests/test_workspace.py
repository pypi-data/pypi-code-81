"""Test module :mod:`vscode.workspace`."""

# Standard library:
import getpass
import os
import typing as t
from pathlib import Path

# 3rd party:
import pytest

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.paths
import jarpyvscode.usersettings
import jarpyvscode.workspace


class WorkspacesSuite:
    """Test functions in the module :mod:`vscode.workspace`."""

    def test_read_valid_code_workspace_file(
        self,
        valid_code_workspace_config_and_file_path: t.Tuple[t.Dict[str, t.Any], str],
    ) -> None:
        """Test reading a ``.code-workspace`` file with valid JSON data."""
        expected_config = valid_code_workspace_config_and_file_path[0]
        actual_config: t.Optional[
            t.Dict[str, t.Any]
        ] = jarpyvscode.workspace.read_code_workspace_file(
            code_workspace_file_path=Path(valid_code_workspace_config_and_file_path[1])
        )
        assert actual_config == expected_config

    def test_read_invalid_code_workspace_file(
        self, invalid_code_workspace_file_path: Path
    ) -> None:
        """Test reading a ``.code-workspace`` file with invalid JSON data."""
        with pytest.raises(ValueError):
            jarpyvscode.workspace.read_code_workspace_file(
                code_workspace_file_path=Path(invalid_code_workspace_file_path)
            )

    @pytest.mark.skipif(
        os.getenv("IS_GITLAB_RUN", 0) == "1",
        reason=(
            "Cannot run this test on GitLab since working with JARROOT is not "
            "possible there."
        ),
    )
    def test_setup_folders(
        self,
        valid_code_workspace_config_and_file_path: t.Tuple[t.Dict[str, t.Any], Path],
    ) -> None:
        """Test to setup the folders in a ``.code-workspace`` file."""
        s = os.sep
        jarroot = jarpyvscode.usersettings.jarroot()
        test_path: Path = valid_code_workspace_config_and_file_path[1].parent / "test"
        if "windows" in c.PLATFORM_LOWER:
            test_path = Path(jarpyvscode.paths.path_backslashed(test_path))
        folders: t.List[t.Dict[str, str]] = [
            {"name": "test", "path": str(test_path)},
            {"name": getpass.getuser(), "path": str(Path.home())},
            {"name": "repos", "path": f"{jarroot}{s}repos"},
        ]
        if Path(f"{jarroot}{s}repos{s}vscode").is_dir():
            folders += [
                {"name": "vscode", "path": f"{jarroot}{s}repos{s}vscode"},
                # {"path": f"{jarroot}{s}repos{s}vscode"},
            ]
        if Path(f"{jarroot}{s}tmp").is_dir():
            folders += [{"name": "tmp", "path": f"{jarroot}{s}tmp"}]
        folders += [
            {"name": "jar", "path": f"{jarroot}{s}repos{s}jar"},
            # {"path": f"{jarroot}{s}repos{s}jar"},
        ]
        expected: t.Tuple[t.Dict[str, t.Any], t.Optional[Path]] = (
            {"folders": folders},
            test_path,
        )
        config: t.Dict[str, t.Any] = valid_code_workspace_config_and_file_path[0]
        result = jarpyvscode.workspace.setup_folders(
            config=config,
            code_workspace_file_path=valid_code_workspace_config_and_file_path[1],
        )
        assert expected == result

        # Now we rename the key "folders" to "fake":
        config["fake"] = config["folders"]
        del config["folders"]

        result = jarpyvscode.workspace.setup_folders(
            config=config,
            code_workspace_file_path=valid_code_workspace_config_and_file_path[1],
        )
        expected = (config, None)
        assert expected == result

    def test_setup_folders_windows_to_windows(self):
        pass
