import threading
import traceback

from typing import List
from abc import abstractmethod
from datetime import datetime

from firebase_admin import firestore
from google.cloud.firestore_v1 import DocumentReference

from boastlabs.functions.execution.exceptions import RetryException, SleepException
from boastlabs.functions.execution.threading import TimedThread
from boastlabs.functions.execution.time import Timer
from boastlabs.functions.execution.events.events import Event
from boastlabs.functions.execution.config import Status
from boastlabs.functions.execution.progress import Progress


class Worker(TimedThread):

    service_name: str
    created_at: datetime
    modified_at: datetime
    status: str
    error: str
    error_stack: str
    exit_status: str
    _progress: Progress

    def __init__(self, timer: Timer, event: Event, doc_ref: DocumentReference, service_name: str):
        TimedThread.__init__(self, timer=timer, event_id=timer.event_id, name=__class__.__name__)

        self.event = event
        self.doc_ref = doc_ref
        self.service_name = service_name

        self.data = {}
        self.read_data()

        self._read_lock = threading.RLock()
        self._write_lock = threading.RLock()

        # Load progress
        if self.doc_ref.collection('progress').document('progress').get().exists:
            self._progress = Progress(
                id='progress',
                progress=self.doc_ref.collection('progress').document('progress').get().to_dict().get('progress', None)
            )
        else:
            self._progress = Progress(id='progress', progress=None)

        self.sleep_duration = 540

    def read_data(self):
        self.data = self.doc_ref.get().to_dict()

        self.created_at = self.data.get('created_at', None)
        self.modified_at = self.data.get('modified_at', None)
        self.status = self.data.get('status', Status.NEW)
        self.error = self.data.get('error', None)
        self.error_stack = self.data.get('error_stack', None)

    def set_created_at(self):
        if self.created_at is None:
            self.doc_ref.update({'created_at': firestore.SERVER_TIMESTAMP})

    def set_modified_at(self):
        self.doc_ref.update({'modified_at': firestore.SERVER_TIMESTAMP})

    def set_status(self, status: str):
        self.doc_ref.update({
            'status': status,
            'modified_at': firestore.SERVER_TIMESTAMP
        })

    def set_error(self, error: Exception):
        error_string = repr(error)
        error_stack = traceback.format_exc()

        self.doc_ref.update({
            'error': error_string,
            'error_stack': error_stack
        })

    def reset(self):
        self.doc_ref.update({
            'error': None,
            'error_stack': None
        })

    def get_sleep_duration(self):
        return self.sleep_duration

    def save_progress(self):
        with self._write_lock:
            self.set_modified_at()
            self.doc_ref.collection('progress').document('progress').set({
                'progress': self._progress.to_dict()
            }, merge=True)

    def get_progress(self, items: List[str]) -> Progress:
        """
        todo: add documentation, mandatory function
        :param items:
        :return:
        """

        # This will basically do a return progress[user_name][organisation][repo][kind]

        with self._read_lock:
            p = self._progress
            for item in items:
                p = p[item]
            return p

    def run(self):
        self.set_created_at()
        self.set_modified_at()

        # Test event.status to figure out what the function has to to
        # It can be only SLEEP or RUN
        if self.status == Status.SLEEP:
            self.set_status(Status.SLEEP)
            duration = self.get_sleep_duration()

            # Wait duration / can be interrupted by timeout
            self.logger.debug(f"# SLEEP START {duration}")
            self.timer.timeout_event.wait(duration)
            self.logger.debug(f"# SLEEP END")

            # Exit with WAITING_RETRY state and resume execution on next call
            self.set_status(Status.WAITING_RETRY)

        if self.status == Status.RUNNING:
            self.logger.debug(f"# RUNNING")
            try:
                self.set_status(Status.RUNNING)
                self.work()
                self.set_status(Status.DONE)
            except RetryException:
                self.set_status(Status.WAITING_RETRY)
            except SleepException:
                self.set_status(Status.WAITING_SLEEP)
            except Exception as e:
                self.set_status(Status.FAILED)
                self.set_error(e)
                raise e

        # TODO: review this
        self.read_data()
        self.exit_status = self.status

    @abstractmethod
    def work(self):
        raise NotImplementedError
