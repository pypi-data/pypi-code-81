"""Test functions for Aracnid Logger functionality.
"""
import os

import pytest

from aracnid_logger import Logger

def test_module_main():
    """Tests that Aracnid Logger was imported successfully.
    """
    config_dir = os.path.dirname(__file__)
    logger = Logger('__main__', config_dir=config_dir)

    assert logger.logger.name == 'root'

def test_module_sub():
    """Tests that Aracnid Logger was imported successfully.
    """
    config_dir = os.path.dirname(__file__)
    logger = Logger(__name__, config_dir=config_dir)

    assert logger.logger.name == __name__

def test_setting_config_file_by_arg(monkeypatch):
    """Tests setting the config file by passing the argument.
    """
    monkeypatch.setenv('LOGGING_CONFIG_FILE', 'logging_config_test.json')
    config_dir = os.path.dirname(__file__)
    logger = Logger(
        '__main__',
        config_filename='logging_config_test.json',
        config_dir=config_dir)

    assert logger.logging_filename == 'logging_config_test.json'

def test_setting_config_file_by_env(monkeypatch):
    """Tests setting the config file by environment variable.
    """
    monkeypatch.setenv('LOGGING_CONFIG_FILE', 'logging_config_test.json')
    config_dir = os.path.dirname(__file__)
    logger = Logger('__main__', config_dir=config_dir)

    assert logger.logging_filename == 'logging_config_test.json'

def test_setting_config_file_by_default(monkeypatch):
    """Test that Aracnid Logger sets a default config filename,
    if environmental variable is missing.
    """
    monkeypatch.delenv('LOGGING_CONFIG_FILE', raising=False)
    config_dir = os.path.dirname(__file__)
    logger = Logger('__main__', config_dir=config_dir)

    assert logger.logging_filename == 'logging_config.json'

def test_setting_config_dir_by_arg(monkeypatch):
    """Tests setting the config dir by passing the argument.
    """
    monkeypatch.delenv('LOGGING_CONFIG_DIR', raising=False)
    config_dir = os.path.dirname(__file__)
    logger = Logger(
        '__main__',
        config_filename='logging_config_test.json',
        config_dir=config_dir)

    assert logger.logging_filename == 'logging_config_test.json'

def test_setting_config_dir_by_env(monkeypatch):
    """Tests setting the config dir by environment variable.
    """
    config_dir = os.path.dirname(__file__)
    monkeypatch.setenv('LOGGING_CONFIG_DIR', config_dir)
    logger = Logger(
        '__main__',
        config_filename='logging_config_test.json')

    assert logger.logging_dir == config_dir

def test_missing_config_file(monkeypatch):
    """Tests that Aracnid Logger was imported successfully.
    """
    monkeypatch.setenv('LOGGING_CONFIG_FILE', 'logging_config_missing.json')
    config_dir = os.path.dirname(__file__)

    with pytest.raises(FileNotFoundError):
        _ = Logger('__main__', config_dir=config_dir)

def test_setting_formatter_by_arg(monkeypatch):
    """Tests setting the formatter by passing the argument.
    """
    monkeypatch.delenv('LOGGING_FORMATTER', raising=False)
    config_dir = os.path.dirname(__file__)
    logger = Logger(
        '__main__',
        config_dir=config_dir,
        formatter='deployed')

    assert logger.formatter == 'deployed'

def test_setting_formatter_by_env(monkeypatch):
    """Tests setting the formatter by environment variable.
    """
    monkeypatch.setenv('LOGGING_FORMATTER', 'deployed')
    config_dir = os.path.dirname(__file__)
    logger = Logger(
        '__main__',
        config_dir=config_dir)

    assert logger.formatter == 'deployed'

def test_setting_formatter_by_default(monkeypatch):
    """Tests setting the formatter by default.
    """
    monkeypatch.delenv('LOGGING_FORMATTER', raising=False)
    config_dir = os.path.dirname(__file__)
    logger = Logger(
        '__main__',
        config_dir=config_dir)

    assert logger.formatter == 'default'
