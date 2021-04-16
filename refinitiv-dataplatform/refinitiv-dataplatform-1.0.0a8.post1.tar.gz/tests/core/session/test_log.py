from refinitiv.dataplatform import log
import refinitiv.dataplatform as rdp
import logging


def test_session_logger():
    session = rdp.DesktopSession("")
    logger = log.get_logger(session.name)

    assert logger == session._logger


def test_get_logger():
    log.get_logger("test_get_logger")


def test_dispose_logger():
    logger = log.get_logger("test_dispose_logger")
    assert logger.handlers

    log.dispose_logger(logger)
    assert not logger.handlers


def test_dispose_logger_name():
    logger_name = "test_dispose_logger_name"
    logger = log.get_logger(logger_name)
    assert logger.handlers

    log.dispose_logger(logger_name)
    assert not logger.handlers


def test_existing_loggers():
    loggers_names = log.existing_loggers()
    prev_len = len(loggers_names)

    assert loggers_names

    log.create_logger("test_existing_loggers")

    loggers_names = log.existing_loggers()
    cur_len = len(loggers_names)

    assert cur_len - prev_len == 1


def test_set_log_level():
    logger_name = "test_set_log_level"
    logger = log.set_log_level(logger_name, logging.DEBUG)
    assert logger.level == logging.DEBUG

    logger = log.set_log_level(logger_name, logging.INFO)
    assert logger.level == logging.INFO


def test_filenamer():
    expected = '\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib.artem'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.artem.9')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715-9-24124-refinitiv.data.platform.lib'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv.data.platform.lib.9')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.9')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib.'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib..9')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib-'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib-.9')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib-'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib-')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib.-'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.-')
    assert name == expected, name

    expected = '\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib-'
    name = log._filenamer('\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib-.')
    assert name == expected, name
