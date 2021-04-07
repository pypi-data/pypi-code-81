import threading
import logging
from etl.execution.exceptions import TimeoutException


class TimeoutEvent(threading.Event):
    pass


class Timer:
    _logger: logging.Logger

    def __init__(self, event_id):
        self.event_id = event_id
        self.timeout_event = TimeoutEvent()
        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.event_id}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def timeout(self):
        self.timeout_event.set()
        self.logger.debug('SIGTIMEOUT')

    def raise_for_timeout(self):
        if self.timeout_event.is_set():
            raise TimeoutException

    def is_timeout(self):
        return self.timeout_event.is_set()
