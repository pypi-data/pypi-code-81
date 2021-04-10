import time
import logging
import traceback

from boastlabs.functions.execution.exceptions import RetryException
from boastlabs.functions.execution.time import Timer
from boastlabs.functions.execution.config import Status
from boastlabs.functions.execution.events.handler import EventHandler
from boastlabs.functions.execution.worker import Worker


class Function:
    def __init__(self, service_name, db, event_path, worker_class: Worker.__class__):

        self.service_name = service_name
        self.db = db
        self.event_path = event_path
        self.worker_class = worker_class

        self.event_ref = db.document(event_path)
        self.parent_ref = self.event_ref.parent.parent

        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.event_ref.id}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def try_run(self, timeout_seconds):
        start = time.time()

        # Handle Event
        # Can raise ExecutionNotAllowedException or RetryException
        event_handler = EventHandler(db=self.db, event_ref=self.event_ref)
        event = event_handler.handle()

        # Init the timer
        timer = Timer(event_id=self.event_ref.id)

        # Create the worker
        worker = self.worker_class(timer=timer, event=event, doc_ref=self.parent_ref, service_name=self.service_name)

        worker.start()

        # Wait TIMEOUT_MILLIS seconds and timeout 30 seconds early
        worker.join(timeout_seconds - 30)

        # Timeout here - from now on we have 30 seconds to finish threads
        timer.timeout()

        if worker.is_alive():
            self.logger.debug('# SIGTIMEOUT Sent')

        # Wait for thread to finish
        worker.join()

        self.logger.debug(f"# Function exited with <{worker.exit_status}>")

        end = time.time()
        duration = end - start
        self.logger.debug(f'# Durations in seconds: {int(duration)}, (start={start}, end={end})')

        # Raise exceptions here so GCP will retry our function
        if worker.exit_status in [Status.WAITING_RETRY, Status.WAITING_SLEEP]:
            raise RetryException

    def run(self, timeout_seconds):
        self.logger.debug("# START")

        try:
            self.try_run(timeout_seconds)
        except RetryException:
            # Exit with exception so GCP will retry the function
            raise
        except Exception:
            # Exit normally, no retry here
            traceback.print_exc()
        finally:
            self.logger.debug("# END")

