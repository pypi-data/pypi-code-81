import logging
import logging.handlers
import os
from datetime import datetime
from importlib import reload

from behave import *

import refinitiv.dataplatform as rdp
import refinitiv.dataplatform.log as rdp_logging
from env import remove_prj_config, remove_user_config, write_prj_config, write_user_config
from refinitiv.dataplatform import configure
from tools import create_obj_with_value_by_path

use_step_matcher("re")


class MyLogHandler(logging.Handler):
    def __init__(self, ctx):
        super().__init__()
        self.context = ctx

    def handle(self, record):
        self.context.record = record
        return super().handle(record)

    def emit(self, record):
        pass


@step('I enabled to log in the file and set (?P<path>.+) to (?P<value>.+)')
def step_impl(context, path, value):
    remove_prj_config()
    remove_user_config()
    config = create_obj_with_value_by_path(path, value)
    write_user_config(config)
    reload(configure)


@step("I use a logger in the Library")
def step_impl(context):
    session = rdp.DesktopSession("")
    session.logger().addHandler(MyLogHandler(context))
    context.logger = session


@when("I pass several comma separated arguments into the logger method")
def step_impl(context):
    logger = context.logger
    logger.info("some", "message", "here")


@then("All the arguments are written to the log, separated by SPACE")
def step_impl(context):
    record = context.record
    assert record


@given("available log levels")
def step_impl(context):
    log_levels = []

    for row in context.table:
        log_levels.append((row['string value'], int(row['integer value'])))

    context.log_levels = log_levels


@when("I set logs\.level to (?P<value>.+)")
def step_impl(context, value):
    logger = context.logger
    try:
        value = int(value)
    except ValueError:
        pass
    logger.set_log_level(value)


@then("All levels higher or equal (?P<value>.+) are logged")
def step_impl(context, value):
    try:
        value = int(value)
    except ValueError:
        pass

    value = rdp_logging.convert_log_level(value)

    log_levels = context.log_levels
    logger = context.logger
    levels_sum = 0
    target_levels_sum = 0
    start_to_sum = False
    for level_str, level_int in log_levels:
        log_level = rdp_logging.convert_log_level(level_int)
        logger.log(log_level, "log message")

        if 'record' in context:
            levels_sum += context.record.levelno
            del context.record

        if log_level == value:
            start_to_sum = True

        if start_to_sum:
            target_levels_sum += log_level

    assert target_levels_sum == levels_sum, f'target: {target_levels_sum}, exists: {levels_sum}'


@then("Logs are not written at all")
def step_impl(context):
    context.logger.error("error message")
    assert "record" not in context, context.record


@when("I use any of logger method to write logs")
def step_impl(context):
    logger = context.logger
    logger.error("error message")
    logger.warning("warning message")
    logger.info("info message")
    logger.debug("debug message")
    logger.trace("trace message")


@then("Logs are written to the console, to the file, level higher or equal 'info'")
def step_impl(context):
    logger = context.logger
    logger = logger.logger()

    has_file_handler = False
    has_stdout_handler = False
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.handlers.RotatingFileHandler):
            has_file_handler = True
        elif isinstance(hdlr, logging.StreamHandler):
            has_stdout_handler = True

    assert has_file_handler
    assert has_stdout_handler
    levelno = context.record.levelno
    assert levelno == logging.INFO, levelno


@when("logs are logged to a file")
def step_impl(context):
    logger = context.logger
    logger.error("error message")


@then("Date, time, and process ID are added to the log file name defined in '(?P<path>.+)' field default to '(?P<default_name>.+)'")
def step_impl(context, path, default_name):
    _name = configure.get_str(path)
    assert _name == default_name

    session = rdp.DesktopSession("")
    logger = session.logger()

    file_handler = None
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.handlers.RotatingFileHandler):
            file_handler = hdlr
            break

    filepath = file_handler.baseFilename
    filename = os.path.basename(filepath)
    date, time, process_id, *name = filename.split("-")
    name = "-".join(name)
    assert date and int(date)
    assert time and int(time)
    assert process_id and int(process_id)
    assert name and name == default_name


@step("After rotating the file - the sequence number is added to the file name")
def step_impl(context):
    session = rdp.DesktopSession('')
    logger = session.logger()

    file_handler = None
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.handlers.RotatingFileHandler):
            file_handler = hdlr
            break

    for i in range(10):
        logger.error(f"error message {i}")
        file_handler.doRollover()

    filepath = rdp_logging._filenamer(file_handler.baseFilename + ".1")
    assert os.path.exists(filepath) is True


@when("I set (?P<path>.+) to (?P<filesize>.+)")
def step_impl(context, path, filesize):
    config = create_obj_with_value_by_path(path, filesize)
    write_prj_config(config)
    reload(configure)


@then("Single log file size will be about (?P<expected_filesize>.+)")
def step_impl(context, expected_filesize):
    logger = context.logger
    rdp_logging.dispose_logger(logger)

    reload(rdp_logging)

    logger = rdp.DesktopSession("")
    logger = logger.logger()

    file_handler = None
    stream_handler = None
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.handlers.RotatingFileHandler):
            file_handler = hdlr
        if isinstance(hdlr, logging.StreamHandler):
            stream_handler = hdlr

    logger.removeHandler(stream_handler)

    expected_filesize = rdp_logging.convert_filesize(expected_filesize)
    max_bytes = file_handler.maxBytes
    assert expected_filesize == max_bytes, max_bytes

    start = 0
    stop = expected_filesize // 100
    for i in range(start, stop + 1):
        logger.info("a" * 30)

    import time
    time.sleep(3)

    filepath = rdp_logging._filenamer(file_handler.baseFilename + ".1")
    assert os.path.exists(filepath) is True, filepath

    filesize = os.path.getsize(filepath)
    assert filesize <= expected_filesize, filesize


@then("Total count of all rotated log files will be no more than (?P<maxfiles>.+)")
def step_impl(context, maxfiles):
    maxfiles = int(maxfiles)

    logger = context.logger
    logger = logger.logger()

    file_handler = None
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.handlers.RotatingFileHandler):
            file_handler = hdlr
            break

    for i in range(maxfiles):
        logger.error(f"error message {i}")
        file_handler.doRollover()

    filepath = rdp_logging._filenamer(file_handler.baseFilename + f".{maxfiles}")
    assert os.path.exists(filepath) is True

    filepath = rdp_logging._filenamer(file_handler.baseFilename + f".{maxfiles + 1}")
    assert os.path.exists(filepath) is False


@step("Default total count of all rotated log files is to (?P<default_maxfiles>.+)")
def step_impl(context, default_maxfiles):
    reload(configure)
    default_maxfiles = int(default_maxfiles)
    max_files_ = configure.get_int(configure.keys.log_max_files)
    assert max_files_ == default_maxfiles, max_files_


@step("Default single log file size is to (?P<default_file_size>.+)")
def step_impl(context, default_file_size):
    reload(configure)
    file_size_ = configure.get_str(configure.keys.log_file_size)
    assert file_size_ == default_file_size, file_size_


@step("Default new rotation cycle will be started to (?P<default_interval>.+) - every midnight")
def step_impl(context, default_interval):
    reload(configure)
    interval = configure.get_str(configure.keys.log_interval)
    assert interval == default_interval, interval


@then("New rotation cycle will be started at every (?P<interval>.+)")
def step_impl(context, interval):
    reload(configure)
    interval_, when_ = rdp_logging.convert_interval(interval)

    if when_ != 's':
        raise Exception(f"Cannot wait that long {interval}")

    logger = context.logger
    logger = logger.logger()
    logger.error("error message before sleep")

    import time
    time.sleep(interval_)

    logger.error("error message after sleep")

    file_handler = None
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.handlers.RotatingFileHandler):
            file_handler = hdlr
            break

    filepath = rdp_logging._filenamer(file_handler.baseFilename + ".1")
    assert os.path.exists(filepath) is True


@step("Default filter is to '(?P<default_filter>.+)'")
def step_impl(context, default_filter):
    reload(configure)
    filter_value = configure.get_str(configure.keys.log_filter)
    assert filter_value == default_filter, filter_value


class Record(object):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


@then("Only (?P<record>.+) that match the (?P<filter_by>.+) filter are written")
def step_impl(context, record, filter_by):
    filterer = rdp_logging.make_filter(filter_by)
    record = Record(record)
    result = filterer(record)
    assert result is True, f"record={record.name}, filter_by={filter_by}"


@when("I create new logger using a module name")
def step_impl(context):
    logger = rdp_logging.create_logger("session:desktop")
    logger.addHandler(MyLogHandler(context))
    context.logger = logger
    logger.error("error message")
    logger.warning("warning message")
    logger.info("info message")
    logger.debug("debug message")


@then("Logs are being written by this logger contain this module name \(i\.e\. \[session:desktop\]\)")
def step_impl(context):
    record = context.record
    assert "session:desktop" in rdp_logging._stdout_formatter.format(record)


@step("Timestamp in ISO format \(\[2020-09-16T07:45:40\.632Z\]\) is used for each log message")
def step_impl(context):
    record = context.record
    now_ = datetime.now()
    date_ = now_.strftime('%Y-%m-%d')
    assert f"[{date_}" in rdp_logging._stdout_formatter.format(record)


@step("Each log message contains log LEVEL name \(i\.e\. \[INFO\]\)")
def step_impl(context):
    record = context.record
    assert "[INFO]" in rdp_logging._stdout_formatter.format(record)


@step("Each log message contains thread ID \(i\.e\. \[20566\]\)")
def step_impl(context):
    record = context.record
    assert str(f"[{record.thread}]") in rdp_logging._stdout_formatter.format(record)


@given("I get a logger in the Library")
def step_impl(context):
    # remove_prj_config()
    # remove_user_config()

    session = rdp.DesktopSession("")
    session.logger().addHandler(MyLogHandler(context))
    context.logger = session.logger()