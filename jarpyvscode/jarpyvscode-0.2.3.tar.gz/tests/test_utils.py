"""Test module :mod:`jarpyvscode.utils`."""

# Standard library:
import os
import typing as t
from pathlib import Path

# 3rd party:
import pytest
from pytest import MonkeyPatch

# local:
import jarpyvscode.constants as c
import jarpyvscode.usersettings
import jarpyvscode.utils


@pytest.mark.skipif(
    os.getenv("IS_GITLAB_RUN", 0) == "1", reason="Cannot run this test on GitLab"
)
class AdaptJarrootInPathSuite:
    test_data_set = (
        pytest.param(
            Path("C:/Users/DUMMY/bla/blubs"),
            Path("C:/Users/DUMMY/bla/blubs"),
            id="no adaption needed",
        ),
        pytest.param(
            Path("C:/Users/jamil/repos/jar"),
            jarpyvscode.usersettings.jarroot() / "repos/jar",
            id="jarpc path forward slashs",
        ),
        pytest.param(
            Path(r"C:\Users\jamil\repos/jar"),
            jarpyvscode.usersettings.jarroot() / "repos/jar",
            id="jarpc path backslashs",
        ),
        pytest.param(
            Path(r"C:\\Users\\jamil\\repos/jar"),
            jarpyvscode.usersettings.jarroot() / "repos/jar",
            id="jarpc path double backslashs",
        ),
        pytest.param(
            Path(jarpyvscode.usersettings.jarroot()),
            jarpyvscode.usersettings.jarroot(),
            id="Current JARROOT to be untouched",
        ),
        pytest.param(
            jarpyvscode.usersettings.jarroot() / "repos/jar",
            jarpyvscode.usersettings.jarroot() / "repos/jar",
            id="Child of current JARROOT to be untouched",
        ),
        pytest.param(
            Path("C:/Users/JamilRaichouni2/repos/assets"),
            jarpyvscode.usersettings.jarroot() / "repos/assets",
            id="T4C path with forward slashs",
        ),
    )

    @pytest.mark.parametrize("input_data, expected", test_data_set)
    def test(self, input_data: str, expected: str) -> None:
        result = Path(
            jarpyvscode.utils.adapt_jarroot_in_path(old_path=input_data, sep="/")
        )
        assert expected == result


test_data_set = [
    pytest.param(
        "jarmac",
        "osx",
        [{}],
        Path.home(),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": None,
                "os": None,
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path("/Users/jamil"),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": None,
                "os": "windows",
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path.home(),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": None,
                "os": "osx",
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path("/Users/jamil"),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": "jarmac",
                "os": "osx",
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path("/Users/jamil"),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": ["jarmac", "dbmac"],
                "os": "osx",
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path("/Users/jamil"),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": "jarmac",
                "os": None,
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path("/Users/jamil"),
    ),
    pytest.param(
        "jarmac",
        "osx",
        [
            {
                "hosts": ["jarmac", "dbmac"],
                "os": None,
                "key": "jarpyvscode.jarroot",
                "val": "/Users/jamil",
            }
        ],
        Path("/Users/jamil"),
    ),
]


@pytest.mark.parametrize("hostname, os, host_settings, expected", test_data_set)
def test_jarroot(
    hostname: str,
    os: str,
    host_settings: t.List[t.Dict[str, t.Any]],
    expected: int,
    monkeypatch: MonkeyPatch,
):
    """Test :func:`jarpyvscode.paths.jarroot`.

    Parameters
    ----------
    hostname
        Monkey patched host name
    os
        Monkey patched operating system
    host_settings
        Monkey patched host settings
    expected
        Expected jarroot
    monkeypatch
        Helper to conveniently monkeypatch host name, operating system and
        host settings.

    """
    monkeypatch.setattr(c, "HOSTNAME", hostname)
    monkeypatch.setattr("jarpyvscode.environment.operating_system", lambda: os)
    monkeypatch.setattr(
        "jarpyvscode.usersettings.read_host_settings", lambda: host_settings
    )
    result: Path = jarpyvscode.usersettings.jarroot()
    assert expected == result
