from tests.test_configs.config_helper import (
    load_and_validate,
    load_and_validate_fails,
    load_config,
)
from pencil_pusher.configs import config_manager


def test_valid():
    """
    Tests that a valid config file does not throw
    any errors when validated
    """
    load_config()
    load_and_validate()


def test_invalid_type():
    """
    tests that a config file with an invalid type
    for sources throws an error
    """
    load_config(sources="wrong")
    load_and_validate_fails()


def test_invalid_element_type():
    """
    tests that a complex type with an invalid
    element type throws an error
    """
    load_config(sources=["path1/", 2])
    load_and_validate_fails()


def test_invalid_name():
    """
    tests that a missing config parameter that is required
    throws an error
    """
    load_config(exclude=["sources"])
    load_and_validate_fails()


def test_get_values():
    """
    tests that config values are loaded properly
    """
    expected = [
        "path1/*",
        "path1/anotherpath/*",
        "path1/anotherpath2/",
        "path1/anotherpath2/file1.py",
    ]

    load_config(sources=expected)
    load_and_validate()

    response = config_manager.get("sources")
    assert len(expected) == len(response)
    for path in expected:
        assert path in response


def test_tilde_in_source():
    """
    Tests that a source does not contain any non relative paths
    i.e. tilde (~)
    """
    load_config(sources=["path1/tets", "~/path2/wrong.py"])
    load_and_validate_fails()
