import time
import logging
import traceback

from etl.execution.config import Status, TIMEOUT_SECONDS
from etl.execution.exceptions import ExecutionNotAllowed, RetryException, SleepException
from etl.execution.events import ExecutionEvent
from etl.execution.time import Timer
from etl.execution.state import State
from etl.execution.worker import NoopWorker


class Process:
    def __init__(self, db, event_path, worker_class):
        self.db = db
        self.event_path = event_path
        self.worker_class = worker_class

        self.event_id = self.event_path.split('/')[-1]
        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.event_id}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def try_run(self):
        start = time.time()

        # Init the timer
        timer = Timer(event_id=self.event_id)

        # Handles event and set the new state
        # Raises ExecutionNotAllowed if execution is not allowed
        event = ExecutionEvent(db=self.db, path=self.event_path)
        event.handle()

        # Grab the state document, also the parent document
        # and figure out if we should run in "no op" mode or "real"
        state = State(db=self.db, job_path=event.event_ref.parent.parent.path)
        if state.etl_job_dict.get('worker_type', None) == 'dummy':
            worker = NoopWorker(timer=timer, state=state, event_id=self.event_id)
        else:
            worker = self.worker_class(timer=timer, state=state, event_id=self.event_id)

        worker.start()

        # Wait TIMEOUT_MILLIS seconds and timeout 30 seconds early
        worker.join(TIMEOUT_SECONDS - 30)

        # Timeout here - from now on we have 30 seconds to finish threads
        timer.timeout()

        if worker.is_alive():
            self.logger.debug('# SIGTIMEOUT Sent')

        # Wait for thread to finish
        worker.join()

        self.logger.debug(f"# Worker joined with {state.status}")

        end = time.time()
        duration = end - start
        self.logger.debug(f'# Durations in seconds {int(duration)}, start={start}, end={end}')

        return state.status

    def run(self):
        self.logger.debug("# START")

        exit_status = None
        try:
            exit_status = self.try_run()
        except ExecutionNotAllowed as e:
            self.logger.error(e)
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
            self.logger.error('# Process exited with Exception.')
        if exit_status == Status.DONE:
            self.logger.debug('# Process exited with success.')
