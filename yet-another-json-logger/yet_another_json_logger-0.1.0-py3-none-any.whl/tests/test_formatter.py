"""Test JSON formatter."""

import getpass
import json
import logging
import os
import socket

import yajl


def test_formatter_does_something():
    record = logging.LogRecord(name='my.logger',
                               level=logging.INFO,
                               pathname='/opt/thing/file.py',
                               lineno=1337,
                               msg='%s says %r',
                               args=('Alice', 'hi!'),
                               exc_info=None)
    formatter = yajl.JsonFormatter()
    formatted = formatter.format(record)
    expected = {'hostname': socket.getfqdn(),
                         'pwd': os.getcwd(),
                         'user': getpass.getuser(),
                         'name': record.name,
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
                         'message': "Alice says 'hi!'"}
    assert formatted == json.dumps(expected)
