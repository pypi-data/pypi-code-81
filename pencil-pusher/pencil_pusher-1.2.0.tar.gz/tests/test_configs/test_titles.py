from tests.test_configs.config_helper import (
    load_and_validate,
    load_and_validate_fails,
    load_config,
)
from pencil_pusher.configs import config_manager


def test_valid():
    """
    Tests that a valid config file contains the required
    parameter titles
    """
    load_config()
    load_and_validate()


def test_invalid_type():
    """
    """
    load_config(titles=3)
    load_and_validate_fails()


def test_invalid_subtype_source():
    """
    """
    load_config(titles=[{"source": 3, "title": "valid"}])
    load_and_validate_fails()


def test_invalid_subtype_title():
    """
    """
    load_config(titles=[{"source": "valid", "title": 2}])
    load_and_validate_fails()


def test_missing_subtype_source():
    """
    """
    load_config(titles=[{"title": "valid"}])
    load_and_validate_fails()


def test_missing_subtype_title():
    """
    """
    load_config(titles=[{"source": "valid"}])
    load_and_validate_fails()


def test_get_titles():
    """
    """
    expected = [{"source": "mysourcefile.py", "title": "wowsuchdocs"}]

    load_config(titles=expected)
    load_and_validate()

    response = config_manager.get("titles")
    assert response == expected
