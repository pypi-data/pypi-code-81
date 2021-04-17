"""Tests for the module :mod:`jarpyvscode.usersettings`."""

# Standard library:
import typing as t

# 3rd party:
import pytest
from pytest import MonkeyPatch

# local:
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.paths
import jarpyvscode.usersettings

test_data_set = [
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": "jarmac", "os": None},
        100,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": ["jarmac", "dbmac"], "os": None},
        100,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": "jarmac", "os": "osx"},
        100,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": ["jarmac", "dbmac"], "os": "osx"},
        100,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": "jarmac", "os": ["osx", "linux"]},
        100,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": ["jarmac", "dbmac"], "os": ["osx", "linux"]},
        100,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": None, "os": "osx"},
        50,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": "dbmac", "os": "osx"},
        50,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {
            "hosts": [
                "dbmac",
            ],
            "os": "osx",
        },
        50,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": "dbmac", "os": ["osx", "linux"]},
        50,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": ["dbmac", "dbmac"], "os": ["osx", "linux"]},
        50,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": None, "os": None},
        10,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {},
        0,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"hosts": None},
        0,
    ),
    pytest.param(
        "jarmac",
        "osx",
        {"os": None},
        0,
    ),
]


@pytest.mark.parametrize("hostname, os, host_setting, expected", test_data_set)
def test_determine_applicability_score(
    hostname: str,
    os: str,
    host_setting: t.Dict[str, t.Any],
    expected: int,
    monkeypatch: MonkeyPatch,
):
    """Test :func:`jarpyvscode.usersettings.determine_applicability_score`.

    Parameters
    ----------
    hostname
        Monkey patched host name
    os
        Monkey patched operating system
    host_setting
        Test object
    expected
        Expected applicability score
    monkeypatch
        Helper to conveniently monkeypatch host name and operating system.

    """
    monkeypatch.setattr(c, "HOSTNAME", hostname)  # type: ignore
    monkeypatch.setattr("jarpyvscode.environment.operating_system", lambda: os)
    result: int = jarpyvscode.usersettings.determine_applicability_score(host_setting)
    assert expected == result
