import importlib
import logging
import sys
from os import environ

from moonspec.state import State


def _journald_logging_supported() -> bool:
    if not hasattr(importlib, 'util'):
        return importlib.find_loader('systemd') is not None
    else:
        return importlib.util.find_spec('systemd') is not None


def _bootstrap_default_logger(logger: logging.Logger) -> None:
    is_debug = environ.get('MOONSPEC_DEBUG') is not None
    log_to_journal = environ.get('MOONSPEC_LOG_SYSTEMD') is not None

    if is_debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger.setLevel(log_level)

    stdout_fmt = logging.Formatter('%(levelname)-8s %(asctime)s %(message)s')

    if log_to_journal is False or False is _journald_logging_supported():
        stdout = logging.StreamHandler()
        stdout.setLevel(log_level)
        stdout.setFormatter(stdout_fmt)

        if hasattr(stdout, 'setStream'):
            stdout.setStream(sys.stdout)

        logger.addHandler(stdout)

        if log_to_journal:
            logger.warning('SystemD logging not available - module <systemd> not found. '
                           'Did you pip install systemd?')
    else:
        # mypy: ignore-missing-imports
        from systemd.journal import JournaldLogHandler  # type: ignore
        handler = JournaldLogHandler()
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        logger.addHandler(handler)

    if is_debug:
        logger.debug('Debug logging is enabled')


def _configure_default_logger() -> None:
    logger = logging.getLogger('moonspec')
    _bootstrap_default_logger(logger)


MOONSPEC_VERSION: str = '0.1.7'

_configure_default_logger()
_MOONSPEC_RUNTIME_STATE: State = State()
