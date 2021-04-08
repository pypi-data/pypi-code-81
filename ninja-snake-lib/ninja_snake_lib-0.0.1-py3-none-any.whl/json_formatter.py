import os
import logging
import socket
from datetime import datetime
from sys import getsizeof
from django.utils import timezone
from django.conf import settings

import json

BUILTIN_ATTRS = {
    'args',
    'asctime',
    'created',
    'exc_info',
    'exc_text',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName',
}


class JSONFormatter(logging.Formatter):
    """JSON log formatter.

    Usage example::

        import logging

        import json_log_formatter

        json_handler = logging.FileHandler(filename='/var/log/my-log.json')
        json_handler.setFormatter(json_log_formatter.JSONFormatter())

        logger = logging.getLogger('my_json')
        logger.addHandler(json_handler)

        logger.info('Sign up', extra={'referral_code': '52d6ce'})

    The log file will contain the following log record (inline)::

        {
            "message": "Sign up",
            "time": "2015-09-01T06:06:26.524448",
            "referral_code": "52d6ce"
        }

    """

    json_lib = json

    def format(self, record):
        message = record.getMessage()
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        # Backwards compatibility: Functions that overwrite this but don't
        # return a new value will return None because they modified the
        # argument passed in.
        if mutated_record is None:
            mutated_record = json_record
        return self.to_json(mutated_record)

    def to_json(self, record):
        """Converts record dict to a JSON string.

        It makes best effort to serialize a record (represents an object as a string)
        instead of raising TypeError if json library supports default argument.
        Note, ujson doesn't support it.

        Override this method to change the way dict is converted to JSON.

        """
        try:
            return self.json_lib.dumps(record, default=_json_serializable)
        # ujson doesn't support default argument and raises TypeError.
        except TypeError:
            return self.json_lib.dumps(record)

    def extra_from_record(self, record):
        """Returns `extra` dict you passed to logger.

        The `extra` keyword argument is used to populate the `__dict__` of
        the `LogRecord`.

        """
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in BUILTIN_ATTRS
        }

    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        """Prepares a JSON payload which will be logged.

        Override this method to change JSON log format.

        :param message: Log message, e.g., `logger.info(msg='Sign up')`.
        :param extra: Dictionary that was passed as `extra` param
            `logger.info('Sign up', extra={'referral_code': '52d6ce'})`.
        :param record: `LogRecord` we got from `JSONFormatter.format()`.
        :return: Dictionary which will be passed to JSON lib.

        """
        if not os.getenv("GN_PYTHON_LIB_APP_NAME"):
            raise RuntimeError("GN_PYTHON_LIB_APP_NAME env required.")
        time = datetime.now()

        if settings.USE_TZ:
            time = timezone.localtime().isoformat()

        full_log = {
            'message': message,
            'time': time,
            'client': os.getenv("GN_PYTHON_LIB_APP_NAME"),
            'configuration': '0.1',
            'priority': record.levelname,
            'request_time': '-',
            'request_method': '-',
            'status': '-',
            'scheme': '-',
            'request_uri': '-',
            'request_length': '-',
            'bytes_sent': '-',
            'remote_addr': '-',
            'http_user_agent': '-',
            'requestQuery': '-',
            'headers': '-',
            'custom': '-'
        }

        if extra.get('request'):
            if not isinstance(extra.get('request'), socket.SocketType):
                request = extra.get('request')
                web_log = {
                    'request_time': '-',
                    'status': '-',
                    'bytes_sent': '-',
                    'request_method': request.method,
                    'scheme': request.scheme,
                    'request_uri': request.META.get('PATH_INFO', '-'),
                    'request_length': getsizeof(request.body),
                    'remote_addr': request.META.get('REMOTE_ADDR', '-'),
                    'http_user_agent': request.META.get('HTTP_USER_AGENT', '-'),
                    'requestQuery': request.META.get('QUERY_STRING', '-'),
                    'headers': dict(request.headers),
                }
                full_log.update(web_log)

            del extra['request']

        if extra.get('server_time'):
            del extra['server_time']

        full_log.update(extra)

        if record.exc_info or record.levelname.lower() == 'exception':
            full_log['exc_info'] = self.formatException(record.exc_info)

        return full_log

    def mutate_json_record(self, json_record):
        """Override it to convert fields of `json_record` to needed types.

        Default implementation converts `datetime` to string in ISO8601 format.

        """
        for attr_name in json_record:
            attr = json_record[attr_name]
            if isinstance(attr, datetime):
                json_record[attr_name] = attr.isoformat()
        return json_record


def _json_serializable(obj):
    try:
        return obj.__dict__
    except AttributeError:
        return str(obj)
