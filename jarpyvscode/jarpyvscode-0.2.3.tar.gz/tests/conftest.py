"""Set environment variable ``TESTRUN``."""

# Standard library:
import json
import typing as t
from pathlib import Path

# 3rd party:
import pytest
from pytest import MonkeyPatch


@pytest.fixture(scope="function")
def invalid_code_workspace_file_path(
    valid_code_workspace_config_and_file_path: t.Tuple[t.Dict[str, t.Any], Path]
) -> Path:
    """Create a temporary and invalid ``.code-workspace`` file."""
    config: t.Dict[str, t.Any] = valid_code_workspace_config_and_file_path[0]
    code_workspace_file_path: Path = valid_code_workspace_config_and_file_path[1]
    code_workspace_file_path.write_text(data=json.dumps(config)[3:], encoding="utf8")
    return code_workspace_file_path


@pytest.fixture()
def set_pytest_env_var(monkeypatch: MonkeyPatch):
    """Set env var describing that test is running.

    .. seealso:: :mod:`jarpyvscode.message_and_dialog`

    """
    monkeypatch.setenv("TESTRUN", "1")


@pytest.fixture(scope="function")
def valid_code_workspace_config_and_file_path(
    tmpdir,  # type: ignore
) -> t.Tuple[t.Dict[str, t.Any], Path]:
    r"""Create a temporary and valid ``.code-workspace`` file.

    The file contains the data listed below. The first folder path is a relative path
    to be made absolute. A specific is that there is a folder entry pointing to a not
    existing directory. Another detail is that the data contains two entries pointing
    to directories with same names.

    The test data is of special interest in the test
    :meth:`tests.test_workspace.WorkspacesSuite.test_setup_folders`

    .. code-block:: json

        {
            "folders": [
                {
                    "path": "./test"
                },
                {
                    "path": "/NOT/EXISTING/DIR"
                },
                {
                    "path": "/HOME/DIRECTORY/OF/TEST/USER"
                },
                {
                    "name": "repos",
                    "path": "/Users/jamil/repos"
                },
                {
                    "path": "C:/Users/jamil/repos/vscode"
                },
                {
                    "path": "C:\\Users\\jamil\\repos\\vscode"
                },
                {
                    "path": "/Users/jamil/Documents/tmp"
                },
                {
                    "path": "C:\\Users\\jamil\\repos\\jar"
                },
                {
                    "path": "/Users/jamil/repos/jar"
                }
            ]
        }

    Parameters
    ----------
    tmpdir
        Temporary directory managed by pytest

    Returns
    -------
    t.Tuple[t.Dict[str, t.Any], Path]
        * Item 0: t.Dictionary with config data.
        * Item 1: Absolute path to the created file.

    """
    tmpdir.mkdir("test")
    config: t.Dict[str, t.Any] = {
        "folders": [
            {"path": "./test"},
            {"path": "/NOT/EXISTING/DIR"},
            {"path": str(Path.home())},
            {"name": "repos", "path": "/Users/jamil/repos"},  # jarmac
            {"path": "C:/Users/jamil/repos/vscode"},  # jarpc
            {"path": "C:\\Users\\jamil\\repos\\vscode"},  # jarpc
            {"path": "/Users/jamil/tmp"},  # jarmac
            {"path": "C:\\Users\\jamil\\repos\\jar"},  # jarpc
            {"path": "/Users/jamil/repos/jar"},  # jarmac
        ]
    }
    code_workspace_file_path: Path = Path(tmpdir.join("valid.code-workspace"))
    code_workspace_file_path.write_text(data=json.dumps(config), encoding="utf8")
    return (config, code_workspace_file_path)


@pytest.fixture(scope="function")
def valid_jar_code_workspace_config_and_file_path_dbmac(
    tmpdir,  # type: ignore
) -> t.Tuple[t.Dict[str, t.Any], Path]:
    r"""Create temporary ``jar.code-workspace`` file as on ``dbmac`` machine.

    Parameters
    ----------
    tmpdir
        Temporary directory managed by pytest

    Returns
    -------
    t.Tuple[t.Dict[str, t.Any], Path]
        * Item 0: Dictionary with config data.
        * Item 1: Absolute path to the created file.

    """
    tmpdir.mkdir("test")
    config: t.Dict[str, t.Any] = {
        "folders": [
            {"name": "jar", "path": "/Users/jamilraichouni/repos/jar"},
            {
                "name": "jar-extensions",
                "path": "/Users/jamilraichouni/repos/vscode/jar-extensions",
            },
        ],
        "settings": {"git.ignoredRepositories": ["/Users/jamilraichouni/repos/vscode"]},
    }
    code_workspace_file_path: Path = Path(tmpdir.join("jar.code-workspace"))
    code_workspace_file_path.write_text(
        data=json.dumps(obj=config, indent=4), encoding="utf8"
    )
    return (config, code_workspace_file_path)


@pytest.fixture(scope="function")
def valid_jar_code_workspace_config_and_file_path_jarmac(
    tmpdir,  # type: ignore
) -> t.Tuple[t.Dict[str, t.Any], Path]:
    r"""Create temporary ``jar.code-workspace`` file as on ``jarmac`` machine.

    Parameters
    ----------
    tmpdir
        Temporary directory managed by pytest

    Returns
    -------
    t.Tuple[t.Dict[str, t.Any], Path]
        * Item 0: Dictionary with config data.
        * Item 1: Absolute path to the created file.

    """
    tmpdir.mkdir("test")
    config: t.Dict[str, t.Any] = {
        "folders": [
            {"name": "jar", "path": "/Users/jamil/repos/jar"},
            {
                "name": "jar-extensions",
                "path": "/Users/jamil/repos/vscode/jar-extensions",
            },
        ],
        "settings": {"git.ignoredRepositories": ["/Users/jamil/repos/vscode"]},
    }
    code_workspace_file_path: Path = Path(tmpdir.join("jar.code-workspace"))
    code_workspace_file_path.write_text(
        data=json.dumps(obj=config, indent=4), encoding="utf8"
    )
    return (config, code_workspace_file_path)
