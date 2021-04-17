"""Tests for the module :mod:`jarpyvscode.strings`."""

# Standard library:
import typing as t
from pathlib import Path

# 3rd party:
import pytest
from pytest import MonkeyPatch

# local:
import jarpyvscode.constants as c
import jarpyvscode.paths
import jarpyvscode.strings


class DecomposeVersionSuite:

    """Test the function :func:`jarpyvscode.strings.decompose_version`."""

    test_data_set = [
        pytest.param(None),
        pytest.param(1),
        pytest.param(1.0),
        pytest.param({}),
        pytest.param([]),
        pytest.param(()),
    ]

    @pytest.mark.parametrize("version", test_data_set)
    def test_invalid_input_types(self, version: str) -> None:
        """Test with multiple invalid inputs."""
        with pytest.raises(TypeError) as excinfo:
            jarpyvscode.strings.decompose_version(version=version)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "The argument 'version' must be a string."

    test_data_set = [
        pytest.param(".1"),
        pytest.param("1."),
        pytest.param(".1.2"),
        pytest.param("1.2."),
        pytest.param("x"),
        pytest.param("x.y"),
        pytest.param("x.y.z"),
    ]

    @pytest.mark.parametrize("version", test_data_set)
    def test_invalid_input_values(self, version: str) -> None:
        """Test with multiple invalid inputs."""
        with pytest.raises(ValueError) as excinfo:
            jarpyvscode.strings.decompose_version(version)
        exception_msg = excinfo.value.args[0]
        expected_msg = (
            f"Cannot decompose software version information from '{version}'!"
        )
        assert exception_msg == expected_msg

    test_data_set = [
        pytest.param("1", {"major": "1", "minor": None, "patch": None}),
        pytest.param("01", {"major": "01", "minor": None, "patch": None}),
        pytest.param("1.2", {"major": "1", "minor": "2", "patch": None}),
        pytest.param("   1.2", {"major": "1", "minor": "2", "patch": None}),
        pytest.param("1.2      ", {"major": "1", "minor": "2", "patch": None}),
        pytest.param("1.2.3", {"major": "1", "minor": "2", "patch": "3"}),
        pytest.param(" 1.2.3", {"major": "1", "minor": "2", "patch": "3"}),
        pytest.param("1.2.3 ", {"major": "1", "minor": "2", "patch": "3"}),
        pytest.param(" 1.2.3 ", {"major": "1", "minor": "2", "patch": "3"}),
    ]

    @pytest.mark.parametrize("version, expected", test_data_set)
    def test_valid_inputs(
        self, version: str, expected: t.Dict[str, t.Optional[str]]
    ) -> None:
        """Test with multiple valid inputs."""
        actual = jarpyvscode.strings.decompose_version(version)
        assert actual == expected


class PopulatePlaceholdersSuite:

    """Test the function :func:`jarpyvscode.strings.fill_placeholders`."""

    test_data_set = [
        pytest.param(None),
        pytest.param(1),
        pytest.param(1.0),
        pytest.param({}),
        pytest.param([]),
        pytest.param(()),
    ]

    @pytest.mark.parametrize("subject", test_data_set)
    def test_invalid_input_types(self, subject: str) -> None:
        """Test with multiple invalid input types."""
        with pytest.raises(TypeError) as excinfo:
            jarpyvscode.strings.fill_placeholders(
                subject=subject, kwargs={}  # type: ignore
            )
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "The argument 'subject' must be a string."

    test_data_set = [
        pytest.param(
            "Hello ${SOMEBODY}!", {"SOMEBODY": "my friend"}, "Hello my friend!"
        ),
        pytest.param(
            "Version: ${MAJOR}.${MINOR}.${PATCH}",
            {"MAJOR": "1", "MINOR": "2", "PATCH": "3"},
            "Version: 1.2.3",
        ),
        pytest.param(
            "Hello ${FIRSTNAME} ${LASTNAME}!",
            {"FIRSTNAME": "Jamil", "LASTNAME": "Raichouni"},
            "Hello Jamil Raichouni!",
        ),
        pytest.param(
            "${DUPLICATE}, ${DUPLICATE}",
            {"DUPLICATE": "duplicated"},
            "duplicated, duplicated",
        ),
        pytest.param(
            "DUPLICATE}, $DUPLICATE}",
            {"DUPLICATE": "duplicated"},
            "DUPLICATE}, $DUPLICATE}",
        ),
    ]

    @pytest.mark.parametrize("subject, kwargs, expected", test_data_set)
    def test_valid_inputs(
        self, subject: str, kwargs: t.Dict[str, str], expected: str
    ) -> None:
        """Test with multiple valid inputs."""
        actual = jarpyvscode.strings.fill_placeholders(subject=subject, **kwargs)
        assert actual == expected


test_data_set = [
    pytest.param(
        "macos",
        "This is a path ${env:MY_ENV_VAR}.",
        str(Path.home()),
        f"This is a path {Path.home()}.",
    ),
    pytest.param(
        "windows",
        "This is a path ${env:MY_ENV_VAR}.",
        str(Path.home()),
        f"This is a path {jarpyvscode.paths.path_backslashed(Path.home())}.",
    ),
]


@pytest.mark.parametrize("platform_lower, val, env_var_val, expected", test_data_set)
def test_fill_environment_variables(
    platform_lower: str,
    val: str,
    env_var_val: str,
    expected: str,
    monkeypatch: MonkeyPatch,
):
    """Test :func:`jarpyvscode.usersettings.fill_environment_variables`."""
    monkeypatch.setattr(c, "PLATFORM_LOWER", platform_lower)  # type: ignore
    monkeypatch.setenv(name="MY_ENV_VAR", value=env_var_val)
    result: str = jarpyvscode.strings.fill_environment_variables(val)
    assert expected == result
