from abc import abstractmethod
import logging
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

from etl.execution.time import Timer


class TimedThread(Thread):

    def __init__(self, timer: Timer, event_id: str, name: str):
        Thread.__init__(self)

        self.timer = timer
        self.event_id = event_id

        self.setName(f"[{event_id}] [{name}]")
        self.logger = self._init_logger()

    def _init_logger(self):
        _logger = logging.getLogger(self.getName())
        _logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        _logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return _logger

    def raise_for_timeout(self):
        if self.timer.is_timeout():
            self.logger.debug('# SIGTIMEOUT received, aborting.')
            self.timer.raise_for_timeout()

    @abstractmethod
    def work(self):
        raise NotImplementedError

    def run(self) -> None:
        self.logger.debug('# START')
        self.raise_for_timeout()

        self.work()
        self.logger.debug('# END')


class Executor(object):

    @classmethod
    def execute(cls, workers, max_workers):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for future in as_completed([executor.submit(worker.run) for worker in workers]):
                if future.exception():
                    raise future.exception()
