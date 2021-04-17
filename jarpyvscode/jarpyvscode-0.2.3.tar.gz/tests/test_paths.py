"""Test module :mod:`jarpyvscode.paths`."""

# Standard library:
import itertools
import typing as t
from getpass import getuser
from pathlib import Path

# 3rd party:
import pytest
from pytest import MonkeyPatch

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.paths

test_data_set: t.List[t.Any] = []
char: str
for char in c.ALPHABET:
    letter_variants = (char, char.lower())
    colon_variants = (":", "%3A")

    letter_combinations = list(itertools.product(letter_variants, repeat=2))
    colon_combinations = list(itertools.product(colon_variants, repeat=2))
    index_combinations = list(itertools.permutations((0, 1)))

    doubled_drive_letter_combinations = []

    for letter_combination in letter_combinations:
        for colon_combination in colon_combinations:
            for index_combination in index_combinations:
                letter_0 = letter_combination[index_combination[0]]
                letter_1 = letter_combination[index_combination[1]]

                colon_0 = colon_combination[index_combination[0]]
                colon_1 = colon_combination[index_combination[1]]

                doubled_drive_letter_combination = (
                    f"{letter_0}{colon_0}{letter_1}{colon_1}"
                )
                doubled_drive_letter_combinations.append(
                    doubled_drive_letter_combination
                )

    doubled_drive_letter_combinations = list(set(doubled_drive_letter_combinations))
    for doubled_drive_letter_combination in doubled_drive_letter_combinations:
        param = pytest.param(
            doubled_drive_letter_combination,
            f"{char.upper()}:",
            id=doubled_drive_letter_combination,
        )
        test_data_set.append(param)


class FixDoubledDriveLetterSuite:
    @pytest.mark.parametrize("string, expected", sorted(test_data_set))
    def test(self, string: str, expected: str) -> None:
        actual = jarpyvscode.paths.fix_doubled_drive_letter(string)
        assert actual == expected


class NormalisePathSuite:
    @pytest.mark.parametrize(
        "input_data, expected_result",
        [
            ("C:/Users/jamil/tmp", "C:/Users/jamil/tmp"),
            (r"c:\Users\jamil\tmp", "C:/Users/jamil/tmp"),
            (r"c:\\Users\\jamil\\tmp", "C:/Users/jamil/tmp"),
            (r"c%3A\Users\jamil\tmp", "C:/Users/jamil/tmp"),
        ],
    )
    def test(self, input_data: str, expected_result: str) -> None:
        result = jarpyvscode.paths.normalise_path(path_string=input_data)
        assert expected_result == result


class PathBackslashedSuite:
    @pytest.mark.parametrize(
        "input_data, expected_result",
        [
            (r"c%3A\Users\jamil\tmp", r"c%3A\Users\jamil\tmp"),
            (r"c:\\Users\\jamil\\tmp", r"c:\Users\jamil\tmp"),
            (r"c:\Users\jamil\tmp", r"c:\Users\jamil\tmp"),
        ],
    )
    def test(self, input_data: str, expected_result: str) -> None:
        result = jarpyvscode.paths.path_backslashed(path_string=input_data)
        assert expected_result == result


class PathDoubleBackslashedSuite:
    @pytest.mark.parametrize(
        "input_data, expected_result",
        [
            (r"c:\\Users\\jamil\\tmp", r"c:\\Users\\jamil\\tmp"),
            (r"c%3A\Users\jamil\tmp", r"c%3A\\Users\\jamil\\tmp"),
            (r"c:/Users/jamil/tmp", r"c:\\Users\\jamil\\tmp"),
        ],
    )
    def test(self, input_data: str, expected_result: str):
        result = jarpyvscode.paths.path_double_backslashed(path_string=input_data)
        assert expected_result == result


class PathLowerDriveLetterSuite:
    @pytest.mark.parametrize(
        "input_data, expected_result",
        [
            (r"c:\\Users\\jamil\\tmp", r"c:\\Users\\jamil\\tmp"),
            (r"C%3A\Users\jamil\tmp", r"c%3A\Users\jamil\tmp"),
            (r"C:/Users/jamil/tmp", r"c:/Users/jamil/tmp"),
            (r"file://C:/Users/jamil/tmp", r"file://c:/Users/jamil/tmp"),
            (r"ftp://C:/Users/jamil/tmp", r"ftp://c:/Users/jamil/tmp"),
            (r"C:", r"c:"),
        ],
    )
    def test(self, input_data: str, expected_result: str) -> None:
        result = jarpyvscode.paths.path_lower_drive_letter(path_string=input_data)
        assert expected_result == result


class PathRemoveDriveLetterSuite:
    @pytest.mark.parametrize(
        "input_data, expected_result",
        [
            ("/tmp", "/tmp"),
            (r"C%3A:\Users\jamil\tmp", r"\Users\jamil\tmp"),
            (r"C:/Users/jamil/tmp", r"/Users/jamil/tmp"),
            (r"file://C:/Users/jamil/tmp", r"file:///Users/jamil/tmp"),
            (r"ftp://C:/Users/jamil/tmp", r"ftp:///Users/jamil/tmp"),
            ("C:", ""),
        ],
    )
    def test(self, input_data: str, expected_result: str) -> None:
        result = jarpyvscode.paths.path_remove_drive_letter(path_string=input_data)
        assert expected_result == result


test_data_set = [
    pytest.param(
        False,
        "linux",
        Path.home() / ".config/Code",
        id="linux_stable",
    ),
    pytest.param(
        True,
        "linux",
        Path.home() / ".config/Code - Insiders",
        id="linux_insiders",
    ),
    pytest.param(
        False,
        "macos",
        Path.home() / "Library/Application Support/Code",
        id="macos_stable",
    ),
    pytest.param(
        True,
        "macos",
        Path.home() / "Library/Application Support/Code - Insiders",
        id="macos_insiders",
    ),
    pytest.param(
        False,
        "windows",
        Path(f"C:/Users/{getuser()}/AppData/Roaming/Code"),
        id="windows_stable",
    ),
    pytest.param(
        True,
        "windows",
        Path(f"C:/Users/{getuser()}/AppData/Roaming/Code - Insiders"),
        id="windows_insiders",
    ),
]


@pytest.mark.parametrize("insiders, platform_lower, expected", test_data_set)
def test_code_dir(
    insiders: bool, platform_lower: str, expected: Path, monkeypatch: MonkeyPatch
):
    """Test path to Visual Studio Code and Visual Studio Code Insiders configuration."""
    if insiders:
        monkeypatch.setenv("IS_INSIDERS", "1")
    else:
        monkeypatch.setenv("IS_INSIDERS", "0")
    monkeypatch.setattr(c, "PLATFORM_LOWER", platform_lower)
    if platform_lower == "windows":
        monkeypatch.setenv("APPDATA", rf"C:\\Users\\{getuser()}\\AppData\\Roaming")
    result: Path = jarpyvscode.paths.code_dir()
    assert expected == result


test_data_set = [
    pytest.param(
        False,
        "linux",
        Path.home() / ".config/Code/User",
        id="linux_stable",
    ),
    pytest.param(
        True,
        "linux",
        Path.home() / ".config/Code - Insiders/User",
        id="linux_insiders",
    ),
    pytest.param(
        False,
        "macos",
        Path.home() / "Library/Application Support/Code/User",
        id="macos_stable",
    ),
    pytest.param(
        True,
        "macos",
        Path.home() / "Library/Application Support/Code - Insiders/User",
        id="macos_insiders",
    ),
    pytest.param(
        False,
        "windows",
        Path(f"C:/Users/{getuser()}/AppData/Roaming/Code/User"),
        id="windows_stable",
    ),
    pytest.param(
        True,
        "windows",
        Path(f"C:/Users/{getuser()}/AppData/Roaming/Code - Insiders/User"),
        id="windows_insiders",
    ),
]


@pytest.mark.parametrize("insiders, platform_lower, expected", test_data_set)
def test_user_dir(
    insiders: bool, platform_lower: str, expected: Path, monkeypatch: MonkeyPatch
):
    """Test path to Visual Studio Code and Visual Studio Code Insiders configuration."""
    if insiders:
        monkeypatch.setenv("IS_INSIDERS", "1")
    else:
        monkeypatch.setenv("IS_INSIDERS", "0")
    monkeypatch.setattr(c, "PLATFORM_LOWER", platform_lower)
    if platform_lower == "windows":
        monkeypatch.setenv("APPDATA", rf"C:\\Users\\{getuser()}\\AppData\\Roaming")
    result: Path = jarpyvscode.paths.user_dir()
    assert expected == result


test_data_set = [
    pytest.param(
        False,
        "linux",
        Path.home()
        / ".config/Code/User/globalStorage/jamilraichouni.jarpyvscode/workspaces",
        id="linux_stable",
    ),
    pytest.param(
        True,
        "linux",
        Path.home()
        / (
            ".config/Code - Insiders/"
            "User/globalStorage/jamilraichouni.jarpyvscode/workspaces"
        ),
        id="linux_insiders",
    ),
    pytest.param(
        False,
        "macos",
        Path.home()
        / (
            "Library/Application Support/Code/"
            "User/globalStorage/jamilraichouni.jarpyvscode/workspaces"
        ),
        id="macos_stable",
    ),
    pytest.param(
        True,
        "macos",
        Path.home()
        / (
            "Library/Application Support/Code - Insiders/"
            "User/globalStorage/jamilraichouni.jarpyvscode/workspaces"
        ),
        id="macos_insiders",
    ),
    pytest.param(
        False,
        "windows",
        Path(
            f"C:/Users/{getuser()}/AppData/Roaming/Code/"
            "User/globalStorage/jamilraichouni.jarpyvscode/workspaces"
        ),
        id="windows_stable",
    ),
    pytest.param(
        True,
        "windows",
        Path(
            f"C:/Users/{getuser()}/AppData/Roaming/Code - Insiders/"
            "User/globalStorage/jamilraichouni.jarpyvscode/workspaces"
        ),
        id="windows_insiders",
    ),
]


@pytest.mark.parametrize("insiders, platform_lower, expected", test_data_set)
def test_workspace_cfgs_dir(
    insiders: bool, platform_lower: str, expected: Path, monkeypatch: MonkeyPatch
):
    """Test path to Visual Studio Code and Visual Studio Code Insiders configuration."""
    if insiders:
        monkeypatch.setenv("IS_INSIDERS", "1")
    else:
        monkeypatch.setenv("IS_INSIDERS", "0")
    monkeypatch.setattr(c, "PLATFORM_LOWER", platform_lower)  # type: ignore
    if platform_lower == "windows":
        monkeypatch.setenv("APPDATA", rf"C:\\Users\\{getuser()}\\AppData\\Roaming")
    result: Path = jarpyvscode.paths.workspace_cfgs_dir()
    assert expected == result
