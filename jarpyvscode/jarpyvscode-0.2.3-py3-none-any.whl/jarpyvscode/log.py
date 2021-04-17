"""Enhance loguru logger."""

# Standard library:
import functools
import logging
import time
import typing as t

# 3rd party:
from loguru import logger

try:
    logger.level("NOTICE")
except ValueError:
    # introduce NOTICE level when not already existing:
    logger.level("NOTICE", no=25, color="<green><bold>")
    logger.__class__.notice = functools.partialmethod(  # type: ignore
        logger.__class__.log, "NOTICE"
    )
# format output for some of the default levels:
logger.level("CRITICAL", color="<bg red><fg black><bold>")
logger.level("INFO", color="<white>")
logger.level("DEBUG", color="<cyan>")
logger.level("TRACE", color="<magenta>")


def get_log_level_from_cli(debug: bool, verbose: int) -> str:
    """Get log level from command line interface (CLI).

    Command line interfaces may accept multiple occurences of an option
    ``-v/--verbose`` to increase the verbosity of the console logger handler.

    The default verbosity for the console handler of this logging module is set to
    ``WARNING``.

    Passing ``-v/ --verbose`` once increases the log level to ``NOTICE``.
    Passing ``-v/ --verbose`` two times increases the log level to ``INFO``.
    Passing ``-v/ --verbose`` three times increases the log level to ``DEBUG``.
    Passing ``-v/ --verbose`` four times increases the log level to ``TRACE``.

    Parameters
    ----------
    debug
        If true, the log level for the console handler will be set to ``DEBUG``,
        otherwise the log level will be computed depending on the value (number of
        ``-v`` respectively ``--verbose`` passed to the command line interface) of
        *verbose*.

    verbose
        Number of option ``-v/--verbose`` passed to the command line interface to
        increase the verbosity of the console logger handler.

    Returns
    -------
    str
        Log level name considering the number of ``-v/ --verbose`` options that have
        been passed to the CLI.

        Possible values:

        * ``"NOTSET"`` (0),
        * ``"DEBUG"`` (10),
        * ``"INFO"`` (20),
        * ``NOTICE`` (25),
        * ``"WARNING"`` (30),
        * ``"ERROR"`` (40), and
        * ``"CRITICAL"`` (50).

    """
    log_level: int = logging.WARNING  # default
    if debug:
        log_level = logging.DEBUG
    elif verbose == 1:
        log_level = logger.level("NOTICE").no
    elif verbose == 2:
        log_level = logging.INFO
    elif verbose == 3:
        log_level = logging.DEBUG
    elif verbose >= 4:
        log_level = logger.level("TRACE").no
    return verbosity_string(log_level)


def logwrap(
    *, entry: bool = True, exit_: bool = True, level: str = "TRACE"
) -> t.Callable:
    """Decorate functions via ``@logger_wraps()``."""

    def wrapper(func: t.Callable) -> t.Callable:  # type: ignore
        name = func.__name__

        @functools.wraps(func)
        def wrapped(
            *args: t.Tuple[t.Any, ...], **kwargs: t.Dict[t.Any, t.Any]
        ) -> t.Any:
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            start: float = time.time()
            result: t.Any = func(*args, **kwargs)
            end: float = time.time()
            duration: float = 1000 * (end - start)
            if exit_:
                logger_.log(
                    level, "Executed '{}' in {} ms (result={})", name, duration, result
                )
            return result

        return wrapped

    return wrapper


def verbosity_string(level: int) -> str:
    """Translate specified log level to a string.

    Parameters
    ----------
    level:
        Log level, possible values:

        * ``logging.NOTSET`` (0),
        * ``TRACE`` (5),
        * ``logging.DEBUG`` (10),
        * ``logging.INFO`` (20),
        * ``NOTICE`` (25),
        * ``logging.WARNING`` (30),
        * ``logging.ERROR`` (40), and
        * ``logging.CRITICAL`` (50).

    Returns
    -------
    str
        Translated log level as verbosity string, possible values:

        * ``"NOTSET"``,
        * ``"TRACE"``,
        * ``"DEBUG"``,
        * ``"INFO"``,
        * ``"NOTICE"``,
        * ``"WARNING"``,
        * ``"ERROR"``, and
        * ``"CRITICAL"``.

    Raises
    ------
    ValueError
        If *level* is not a value out of

        * ``logging.NOTSET`` (0),
        * ``TRACE`` (5),
        * ``logging.DEBUG`` (10),
        * ``logging.INFO`` (20),
        * ``NOTICE`` (25),
        * ``logging.WARNING`` (30),
        * ``logging.ERROR`` (40), and
        * ``logging.CRITICAL`` (50).

    """
    verbosity_string = ""
    if level == logging.NOTSET:  # 0
        verbosity_string = "NOTSET"
    elif level == logger.level("TRACE").no:  # 5
        verbosity_string = "TRACE"
    elif level == logging.DEBUG:  # 10
        verbosity_string = "DEBUG"
    elif level == logging.INFO:  # 20
        verbosity_string = "INFO"
    elif level == logger.level("NOTICE").no:  # 25
        verbosity_string = "NOTICE"
    elif level == logging.WARNING:  # 30
        verbosity_string = "WARNING"
    elif level == logging.ERROR:  # 40
        verbosity_string = "ERROR"
    elif level == logging.CRITICAL:  # 50
        verbosity_string = "CRITICAL"
    else:
        raise ValueError(f"Invalid value {level} for the parameter 'level'!")
    return verbosity_string
