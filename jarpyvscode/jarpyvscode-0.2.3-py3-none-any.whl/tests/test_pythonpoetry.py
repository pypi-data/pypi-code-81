"""Tests for the module :mod:`jarpyvscode.pythonpoetry`."""

# Standard library:
import typing as t
from pathlib import Path

# 3rd party:
import py.path
import pytest
from pytest import MonkeyPatch

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.projects.pythonpoetry
import jarpyvscode.utils


@pytest.fixture(scope="function")
def project_path(tmpdir: py.path.local) -> Path:
    path: Path = Path(tmpdir.mkdir("test_project"))
    return path


test_data_set = [
    pytest.param(
        "jarmac",
        "osx",
        "macos",
        "DEBUG=0\nPYTHONPATH=/Users/jamil/repos/jarpyvscode\n",
        "DEBUG=0\nPYTHONPATH=/Users/jamil/repos/jarpyvscode\n",
        Path("/Users/jamil"),
        [Path("C:\\Users\\jamil")],
        id="macos -> macos",
    ),
    pytest.param(
        "jarpc",
        "windows",
        "windows",
        "DEBUG=0\nPYTHONPATH=/Users/jamil/repos/jarpyvscode\n",
        "DEBUG=0\nPYTHONPATH=C:\\Users\\jamil\\repos\\jarpyvscode\n",
        Path("C:\\Users\\jamil"),
        [Path("/Users/jamil"), Path("/Users/jamilraichouni")],
        id="macos -> windows",
    ),
]


@pytest.mark.parametrize(
    (
        "hostname, os, platform_lower, env_file_content, "
        "expected, jarroot, possible_foreign_jarroots"
    ),
    test_data_set,
)
def test_setup_environment_variables_definition_file(
    hostname: str,
    os: str,
    platform_lower: str,
    env_file_content: str,
    expected: str,
    jarroot: Path,
    possible_foreign_jarroots: t.List[Path],
    project_path: Path,
    monkeypatch: MonkeyPatch,
):
    env_file_path: Path = Path(project_path / ".env")
    env_file_path.write_text(env_file_content)
    project = jarpyvscode.projects.pythonpoetry.Project(path=project_path)
    monkeypatch.setattr(c, "HOSTNAME", hostname)
    monkeypatch.setattr("jarpyvscode.environment.operating_system", lambda: os)
    monkeypatch.setattr(c, "PLATFORM_LOWER", platform_lower)
    monkeypatch.setattr("jarpyvscode.usersettings.jarroot", lambda: jarroot)
    monkeypatch.setattr(
        "jarpyvscode.usersettings.possible_foreign_jarroots",
        lambda: possible_foreign_jarroots,
    )
    project.setup_environment_variables_definition_file()
    result: str = env_file_path.read_text()
    assert expected == result
