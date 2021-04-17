"""Test the module :mod:`jarpyvscode.log`."""

# Standard library:
import logging
import logging.handlers

# 3rd party:
import pytest
from loguru import logger

# local:
from jarpyvscode.log import get_log_level_from_cli, verbosity_string


@pytest.mark.parametrize(
    "debug, verbose, expected_result",
    (
        pytest.param(False, 0, "WARNING", id="--no-debug, count: 0, level: WARNING"),
        pytest.param(
            False,
            1,
            "NOTICE",
            id="--no-debug, count: 1, level: NOTICE",
        ),
        pytest.param(False, 2, "INFO", id="--no-debug, count: 2, level: INFO"),
        pytest.param(False, 3, "DEBUG", id="--no-debug, count: 3, level: DEBUG"),
        pytest.param(False, 4, "TRACE", id="--no-debug, count: 4, level: TRACE"),
        pytest.param(False, 5, "TRACE", id="--no-debug, count: 5, level: TRACE"),
        pytest.param(True, 0, "DEBUG", id="--debug, count: 0, level: DEBUG"),
        pytest.param(True, 1, "DEBUG", id="--debug, count: 1, level: DEBUG"),
        pytest.param(True, 2, "DEBUG", id="--debug, count: 2, level: DEBUG"),
        pytest.param(True, 3, "DEBUG", id="--debug, count: 3, level: DEBUG"),
        pytest.param(True, 4, "DEBUG", id="--debug, count: 4, level: DEBUG"),
        pytest.param(True, 5, "DEBUG", id="--debug, count: 5, level: DEBUG"),
    ),
)
@pytest.mark.log
def test_get_log_level_from_cli(debug: bool, verbose: int, expected_result: int):
    """Test getting the log level via a CLI."""
    result = get_log_level_from_cli(debug=debug, verbose=verbose)
    assert result == expected_result


@pytest.mark.parametrize(
    "level, expected_result",
    (
        pytest.param(logging.NOTSET, "NOTSET", id="NOTSET"),
        pytest.param(logger.level("TRACE").no, "TRACE", id="TRACE"),
        pytest.param(logging.DEBUG, "DEBUG", id="DEBUG"),
        pytest.param(logging.INFO, "INFO", id="INFO"),
        pytest.param(logger.level("NOTICE").no, "NOTICE", id="NOTICE"),
        pytest.param(logging.WARNING, "WARNING", id="WARNING"),
        pytest.param(logging.ERROR, "ERROR", id="ERROR"),
        pytest.param(logging.CRITICAL, "CRITICAL", id="CRITICAL"),
        pytest.param(60, None, id="None"),
    ),
)
@pytest.mark.log
def test_verbosity_string(level: int, expected_result: str):
    """Test the conversion from logging level (int) to string."""
    if level in (
        logging.NOTSET,
        logger.level("TRACE").no,
        logging.DEBUG,
        logging.INFO,
        logger.level("NOTICE").no,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ):
        result = verbosity_string(level=level)
        assert result == expected_result
    else:
        with pytest.raises(ValueError) as excinfo:
            verbosity_string(level=level)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == f"Invalid value {level} for the parameter 'level'!"
