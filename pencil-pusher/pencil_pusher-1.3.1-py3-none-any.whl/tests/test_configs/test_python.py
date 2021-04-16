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


def test_not_defined():
    """
    Tests that a this config is optional
    """
    load_config(exclude=["python"])
    load_and_validate()


def test_invalid_type():
    """
    """
    load_config(python=3)
    load_and_validate_fails()


def test_invalid_subtype_init():
    """
    """
    load_config(
        python={
            "include_init_files": "no",
            "include_main_file": False,
            "module": "mymodule",
        }
    )
    load_and_validate_fails()


def test_invalid_subtype_main():
    """
    """
    load_config(
        python={
            "include_init_files": False,
            "include_main_file": "no",
            "module": "mymodule",
        }
    )
    load_and_validate_fails()


def test_invalid_subtype_module():
    """
    """
    load_config(
        python={
            "include_init_files": False,
            "include_main_file": False,
            "module": 6,
        }
    )
    load_and_validate_fails()


def test_missing_subtype_main():
    """
    """
    load_config(python={"include_init_files": False, "module": "mymod"})
    load_and_validate()


def test_missing_subtype_init():
    """
    """
    load_config(python={"include_main_file": False, "module": "mymod"})
    load_and_validate()


def test_missing_subtype_module():
    """
    """
    load_config(
        python={"include_main_file": False, "include_init_files": False}
    )
    load_and_validate()


def test_get_python():
    """
    """
    expected = {
        "include_init_files": True,
        "include_main_file": True,
        "module": "mymod",
    }

    load_config(python=expected)
    load_and_validate()

    response = config_manager.get("python")
    assert response == expected


def test_get_python_default():
    """
    """
    load_config(exclude=["python"])
    load_and_validate()

    response = config_manager.get("python")
    assert response is None
