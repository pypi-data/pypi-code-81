import traceback

from google.cloud import firestore_v1

import threading
from typing import List
from datetime import datetime

from firebase_admin import firestore

from etl.execution.config import Status
from etl.execution.progress import Progress


class State(object):

    active: bool
    status: str
    api_version: int
    created_at: datetime
    modified_at: datetime

    _progress: Progress

    def __init__(self, db, job_path):
        self.db = db

        self.job_doc = db.document(job_path)
        self.etl_job_doc = self.job_doc.parent.parent
        self.fiscal_year_doc = self.etl_job_doc.parent.parent
        self.provider_doc = self.fiscal_year_doc.parent.parent

        self.job_dict = self.job_doc.get().to_dict()
        self.etl_job_dict = self.etl_job_doc.get().to_dict()
        self.provider_dict = self.provider_doc.get().to_dict()
        self.fiscal_year_dict = self.fiscal_year_doc.get().to_dict()

        self.active = self.job_dict.get('active', False)
        self.status = self.job_dict.get('status', Status.NEW)
        self.created_at = self.job_dict.get('created_at', None)
        self.modified_at = self.job_dict.get('modified_at', None)

        self.fy_start_date = datetime.strptime(self.fiscal_year_dict['start_date'], '%Y-%m-%d')
        self.fy_end_date = datetime.strptime(self.fiscal_year_dict['end_date'], '%Y-%m-%d')

        self._read_lock = threading.RLock()
        self._write_lock = threading.RLock()

        # Load progress
        if self.job_doc.collection('progress').document('progress').get().exists:
            self._progress = Progress(
                id='progress',
                progress=self.job_doc.collection('progress').document('progress').get().to_dict().get('progress', None))
        else:
            self._progress = Progress(id='progress', progress=None)

        # print('# Progress', json.dumps(self._progress.to_dict()))

    def set_created_at(self):
        if self.created_at is None:
            self.created_at = self.job_doc.update({'created_at': firestore.SERVER_TIMESTAMP})

    def set_modified_at(self):
        self.modified_at = self.job_doc.update({'modified_at': firestore.SERVER_TIMESTAMP})
        self.etl_job_doc.update({'modified_at': firestore.SERVER_TIMESTAMP})

    def set_active(self, active: bool):
        self.active = active
        self.job_doc.update({'active': active})

    def set_status(self, status: str, error=None):
        # TODO: fix me
        @firestore_v1.transactional
        def update_status_in_transaction(transaction):

            etl_job_event_ref = self.etl_job_doc.collection('events').document()
            transaction.update(self.job_doc, {'active': False, 'status': Status.DONE})
            transaction.update(self.etl_job_doc, {'status': Status.DONE})
            transaction.set(etl_job_event_ref, {})

        # update_status_in_transaction(transaction=firestore_v1.Transaction(client=self.db, max_attempts=10))

        self.status = status

        self.job_doc.update({'status': status})

        if status == Status.DONE:
            update_status_in_transaction(transaction=firestore_v1.Transaction(client=self.db, max_attempts=10))
            #
            # self.job_doc.update({'active': False})
            # self.etl_job_doc.collection('events').add({})
        if status == Status.FAILED:
            error_string = repr(error)
            error_stack = traceback.format_exc()

            self.job_doc.update({'active': False, 'error': error_string, 'error_stack': error_stack})
            self.etl_job_doc.update({'status': status, 'error': error_string, 'error_stack': error_stack})

        self.etl_job_doc.update({'status': status})

    def get_last_execution_date(self):
        """Gets last executed date from previous jobs.
        Query files in descending by created_at and get the last executed time.

        Returns:
            last_executed_date:datetime object
        """
        query = self.etl_job_doc.parent.order_by(u'created_at', direction=firestore.Query.DESCENDING).limit(2)
        for result in query.stream():
            # Exclude the current job ID and include previous job
            if result.id != self.etl_job_doc.id:
                return result.to_dict()['created_at']
        return None

    def save_progress(self):
        with self._write_lock:
            self.set_modified_at()
            self.job_doc.collection('progress').document('progress').set(
                {'progress': self._progress.to_dict()},
                merge=True
            )

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

    def get_sleep_duration(self):
        return 0
