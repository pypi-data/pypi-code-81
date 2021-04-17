"""Test module :mod:`jarpyvscode.project`."""

# Standard library:
import tempfile
import typing as t
from pathlib import Path

# 3rd party:
import pytest
from pytest import MonkeyPatch

# local:
import jarpyvscode.project

test_data_set = [
    pytest.param(
        str(Path.home() / "THIS_PROJECT_NAME_WILL_NEVER_EXIST"),
        "",
        Path.home() / "THIS_PROJECT_NAME_WILL_NEVER_EXIST",
        id="Valid full path (valid parent dir and project name)",
    ),
    pytest.param(
        str("THIS_PROJECT_NAME_WILL_NEVER_EXIST"),
        "",
        Path.home() / "THIS_PROJECT_NAME_WILL_NEVER_EXIST",
        id="Valid project name but no configured outputPath",
    ),
    pytest.param(
        str("THIS_PROJECT_NAME_WILL_NEVER_EXIST"),
        tempfile.gettempdir(),
        Path(tempfile.gettempdir()) / "THIS_PROJECT_NAME_WILL_NEVER_EXIST",
        id="Valid project name with valid configured outputPath",
    ),
    pytest.param(
        str("THIS_PROJECT_NAME_WILL_NEVER_EXIST"),
        "/Volumes",
        None,
        id="Valid project name with invalid configured outputPath",
    ),
    pytest.param(
        str(Path.home() / "THIS_PROJECT_NAME IS_INVALID_BECAUSE_OF_THE_BLANK"),
        "",
        None,
        id="Invalid full path (valid parent dir and invalid project name)",
    ),
    pytest.param(
        str("THIS_PROJECT_NAME IS_INVALID_BECAUSE_OF_THE_BLANK"),
        "",
        None,
        id="Invalid project name but no configured outputPath",
    ),
    pytest.param(
        str("THIS_PROJECT_NAME IS_INVALID_BECAUSE_OF_THE_BLANK"),
        tempfile.gettempdir(),
        None,
        id="Invalid project name with valid configured outputPath",
    ),
]


@pytest.mark.parametrize("name_or_path, output_path_overwrite, expected", test_data_set)
def test_compute_path(
    name_or_path: str,
    output_path_overwrite: str,
    expected: t.Optional[Path],
    monkeypatch: MonkeyPatch,
):
    """Test the function :func:`jarpyvscode.project.compute_path`."""
    monkeypatch.setattr(
        "jarpyvscode.usersettings.read_user_setting",
        lambda key_chain: output_path_overwrite,
    )
    result: t.Optional[Path] = jarpyvscode.project.compute_path(
        name_or_path=name_or_path
    )
    assert expected == result
