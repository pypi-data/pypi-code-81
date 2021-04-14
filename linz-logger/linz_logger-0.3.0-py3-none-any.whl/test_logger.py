"""
Tests for the hello() function.
"""

import json

from .logger import get_log


def test_hello_without_name():
    """Test with no parameter."""
    assert get_log() is not None


def test_trace(capsys):
    """Test trace level"""
    get_log().trace("abc")
    stdout, _ = capsys.readouterr()
    log = json.loads(stdout)
    assert log["level"] == 10
    assert log["msg"] == "abc"
