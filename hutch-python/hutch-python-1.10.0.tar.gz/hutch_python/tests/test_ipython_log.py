import logging
import sys

import pytest

from hutch_python.ipython_log import IPythonLogger

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def fake_ipython():
    # Clear the sys errors, potentially from previous tests
    try:
        del sys.last_type
        del sys.last_value
        del sys.last_traceback
    except AttributeError:
        pass
    return FakeIPython()


class FakeIPython:
    def __init__(self):
        self.In = ['']
        self.Out = {}
        self.user_ns = dict(In=self.In, Out=self.Out)

    def add_line(self, in_line, out_line=None):
        self.In.append(in_line)
        if out_line is not None:
            self.Out[len(self.In)-1] = out_line


@pytest.mark.timeout(5)
def test_ipython_logger(log_queue, fake_ipython):
    logger.debug('test_ipython_logger')
    ipylog = IPythonLogger(fake_ipython)
    while not log_queue.empty():
        log_queue.get(block=False)
    # Sanity check: make sure our queue handler works
    logger.debug('hello')
    assert 'hello' in log_queue.get().getMessage()
    # We should do nothing if log gets called too early
    ipylog.log()
    assert log_queue.empty()
    # One logged In, no output
    fake_ipython.add_line('print(5)')
    ipylog.log()
    assert 'In  [1]: print(5)' in log_queue.get(block=False).getMessage()
    assert log_queue.empty()
    # One logged In, one Out
    fake_ipython.add_line('1 + 1', 2)
    ipylog.log()
    assert 'In  [2]: 1 + 1' in log_queue.get(block=False).getMessage()
    assert 'Out [2]: 2' in log_queue.get(block=False).getMessage()
    assert log_queue.empty()
    # Log an error
    fake_ipython.add_line('1/0')
    try:
        1/0
    except ZeroDivisionError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
    sys.last_type = exc_type
    sys.last_value = exc_value
    sys.last_traceback = exc_traceback
    ipylog.log()
    assert 'In  [3]: 1/0' in log_queue.get(block=False).getMessage()
    assert not log_queue.empty()
    # Error with the ipython_log module will be logged
    while not log_queue.empty():
        log_queue.get(block=False)
    ipylog.In = None
    ipylog.log()
    assert 'Logging error' in log_queue.get(block=False).getMessage()
