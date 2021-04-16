import refinitiv.dataplatform.log as session_logging
import logging


def test_convert_log_level_str():
    log_level = session_logging.convert_log_level('DEBUG')
    assert logging.DEBUG == log_level

    log_level = session_logging.convert_log_level('debug')
    assert logging.DEBUG == log_level

    log_level = session_logging.convert_log_level('warn')
    assert logging.WARN == log_level

    log_level = session_logging.convert_log_level('silent')
    assert logging.CRITICAL == log_level


def test_convert_log_level_int():
    log_level = session_logging.convert_log_level(logging.DEBUG)
    assert logging.DEBUG == log_level

    log_level = session_logging.convert_log_level(2)
    assert logging.INFO == log_level

    log_level = session_logging.convert_log_level(5)
    assert logging.CRITICAL == log_level


def test_convert_log_default():
    log_level = session_logging.convert_log_level("")
    assert logging.INFO == log_level
