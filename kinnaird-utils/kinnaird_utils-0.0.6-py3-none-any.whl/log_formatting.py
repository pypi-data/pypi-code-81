import logging


def set_stream_logger(name="kinnaird_utils", level=logging.DEBUG, format_string=None):  # pylint: disable=redefined-outer-name
    """
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all cloudsplaining messages to ``stdout``.
        >>> import kinnaird_utils
        >>> kinnaird_utils.log_formatting.set_stream_logger('cloudsplaining.scan', logging.INFO)
    :type name: string
    :param name: Log name
    :type level: int
    :param level: Logging level, e.g. ``logging.INFO``
    :type format_string: str
    :param format_string: Log message format
    """
    # remove existing handlers. since NullHandler is added by default
    handlers = logging.getLogger(name).handlers
    for handler in handlers:  # pylint: disable=redefined-outer-name
        logging.getLogger(name).removeHandler(handler)
    if format_string is None:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
    logger = logging.getLogger(name)  # pylint: disable=redefined-outer-name
    logger.setLevel(level)
    handler = logging.StreamHandler()  # pylint: disable=redefined-outer-name
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)  # pylint: disable=redefined-outer-name
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def set_log_level(verbose: int):
    """
    Set Log Level based on click's count argument.

    Default log level to critical; otherwise, set to: warning for -v, info for -vv, debug for -vvv

    :param verbose: integer for verbosity count.
    :return:
    """
    if verbose == 1:
        set_stream_logger(level=getattr(logging, "WARNING"))
    elif verbose == 2:
        set_stream_logger(level=getattr(logging, "INFO"))
    elif verbose >= 3:
        set_stream_logger(level=getattr(logging, "DEBUG"))
    else:
        set_stream_logger(level=getattr(logging, "CRITICAL"))


def set_log_format_to_simple_warning(name: str, level: int = logging.WARNING):
    """A basic wrapper around set_stream_logger that sets the log formatter to a simple formatted warning"""
    format_string = "[%(levelname)s] %(message)s"
    set_stream_logger(name=name, level=level, format_string=format_string)
