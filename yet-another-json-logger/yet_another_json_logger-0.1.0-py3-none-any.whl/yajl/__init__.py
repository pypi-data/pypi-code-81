"""
Yet another JSON logger.

Complete with opinionated decisions and hardcoded personal preferences.
"""

from functools import wraps
import getpass
import logging
import os
import socket
import traceback

from types import TracebackType
from typing import Any, Callable, Dict, List, Type, Union

__all__ = ('JsonFormatter', 'JSON', 'JSONType', 'ExcSeraliser')

__version__ = '0.1.0'

_JT3 = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
_JT2 = Union[str, int, float, bool, None, Dict[str, _JT3], List[_JT3]]
_JT1 = Union[str, int, float, bool, None, Dict[str, _JT2], List[_JT2]]
_JT0 = Union[str, int, float, bool, None, Dict[str, _JT1], List[_JT1]]
JSONType = Union[str, int, float, bool, None, Dict[str, _JT0], List[_JT0]]
JSON = Dict[str, JSONType]

ExcSeraliser = Callable[[Type[Exception], Exception, TracebackType], JSON]

_JSON_LIBRARIES = ('orjson', 'ujson', 'rapidjson', 'json')
_JSON_IS_BINARY = (True, False, False, False)
_DECODE: bool

for json_library, json_binary in zip(_JSON_LIBRARIES, _JSON_IS_BINARY):
    try:
        json = __import__(json_library)
    except ModuleNotFoundError:
        pass
    else:
        _DECODE = json_binary
        break


def _exc_serialiser(exc_class: Type[Exception],
                    exc: Exception,
                    tb: TracebackType) -> JSON:
    """
    Simple exception serialisation strategy.

    Preserves exceptions as an object with three keys:
      - type: exception type module and qualname, joined with a period
      - str: string representation of the exception
      - traceback: newline joined traceback

    :param exc_class: Exception class
    :param exc: Exception instance
    :param tb: Exception traceback
    :return: JSON-friendly serialised exception
    """
    return {'type': f'{exc_class.__module__}.{exc_class.__qualname__}',
            'str': str(exc),
            'traceback': '\n'.join(traceback.format_tb(tb))}


class JsonFormatter(logging.Formatter):
    """JSON logging formatter."""

    @wraps(logging.Formatter.__init__)
    def __init__(self,
                 *args: Any,
                 exc_key: str = 'exception',
                 exc_serialiser: ExcSeraliser = _exc_serialiser,
                 base_json: Callable[[], JSON] = None,
                 **kwargs: Any) -> None:
        """
        Format log records as JSON.

        See logging.Formatter for default args and kwargs spec.

        :param args: See logging.Formatter
        :param exc_key: Serialised exception JSON key
        :param exc_serialiser: Exception serialiser
        :param base_json: Base JSON to use for logging every record
        :param kwargs See logging.Formatter:
        """
        super().__init__(*args, **kwargs)

        self._exc_key = exc_key
        self._exc_serialiser = exc_serialiser
        if base_json is not None:
            self._base = base_json
        else:
            _static_base = {'hostname': socket.getfqdn(),
                            'pwd': os.getcwd(),
                            'user': getpass.getuser()}
            self._base = lambda: _static_base

    def _format(self, record: logging.LogRecord, formatted: str) -> JSON:
        """
        Format the specified record as JSON-friendly structure.

        :param record: Logging record
        :param formatted: Default formatter formatted message
        :return: JSON-friendly structure
        """
        base = self._base()
        if record.exc_info is not None:
            base[self._exc_key] = self._exc_serialiser(*record.exc_info)

        base.update({'name': record.name,
                     'module': record.module,
                     'level': {'name': record.levelname,
                               'number': record.levelno},
                     'file': {'path': record.pathname,
                              'filename': record.filename,
                              'line': record.lineno,
                              'func': record.funcName},
                     'timestamp': {'abs': record.created,
                                   'rel': record.relativeCreated},
                     'proc': {'id': record.process,
                              'name': record.processName},
                     'thread': {'id': record.thread,
                                'name': record.threadName},
                     'message': formatted})

        return base

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as JSON.

        :param record: Logging record
        :return: JSON string
        """
        formatted = json.dumps(self._format(record, super().format(record)))
        if _DECODE:
            return formatted.decode()
        return formatted
