import time
import logging
import traceback

from boastlabs.functions.retriable.execution.exceptions import RetryException, SleepException
from boastlabs.functions.retriable.execution.config import Status
from boastlabs.functions.retriable.execution.events.handling import EventHandling
from boastlabs.functions.retriable.execution.time import Timer
from boastlabs.functions.retriable.execution.state import State
from boastlabs.functions.retriable.execution.worker import TestWorker


class Function:
    def __init__(self, service_name, db, event_path, worker_class=TestWorker):

        self.service_name = service_name
        self.db = db
        self.event_path = event_path
        self.worker_class = worker_class

        self.event_ref = db.document(event_path)
        self.parent_ref = self.event_ref.parent.parent

        self.event_id = self.event_ref.id
        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.event_id}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def try_run(self, timeout_seconds):
        start = time.time()

        # Init the timer
        timer = Timer(event_id=self.event_id)

        # Handles event and set the new state
        # Can raise ExecutionNotAllowed, DocumentNotFound, HandlerNotFound
        event_handler = EventHandling(db=self.db, event_ref=self.event_ref)
        event_handler.handle()

        # Grab the state document, also the parent document
        # and figure out if we should run in "no op" mode or "real"
        # This is just for debug purposes
        state = State(service_name=self.service_name, db=self.db, job_ref=self.parent_ref)

        if state.etl_job_dict.get('worker_type', None) == 'dummy':
            worker = TestWorker(timer=timer, state=state, event_id=self.event_id)
        else:
            worker = self.worker_class(timer=timer, state=state, event_id=self.event_id)

        worker.start()

        # Wait TIMEOUT_MILLIS seconds and timeout 30 seconds early
        worker.join(timeout_seconds - 30)

        # Timeout here - from now on we have 30 seconds to finish threads
        timer.timeout()

        if worker.is_alive():
            self.logger.debug('# SIGTIMEOUT Sent')

        # Wait for thread to finish
        worker.join()

        self.logger.debug(f"# Worker joined with {state.status}")

        end = time.time()
        duration = end - start
        self.logger.debug(f'# Durations in seconds: {int(duration)}, (start={start}, end={end})')

        return state.status

    def run(self, timeout_seconds):
        self.logger.debug("# START")

        exit_status = None
        try:
            exit_status = self.try_run(timeout_seconds)
        except Exception:
            traceback.print_exc()
        finally:
            self.logger.debug("# END")

        # Raise exceptions here so GCP will retry our function
        if exit_status == Status.WAITING_RETRY:
            raise RetryException
        if exit_status == Status.WAITING_SLEEP:
            raise SleepException
        if exit_status == Status.FAILED:
            self.logger.error('# Function exited with Exception.')
        if exit_status == Status.DONE:
            self.logger.debug('# Function exited with success.')
