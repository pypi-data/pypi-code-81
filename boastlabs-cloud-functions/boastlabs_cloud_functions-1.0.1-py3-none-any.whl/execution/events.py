import logging
import semantic_version

from google.cloud import firestore_v1

from etl.execution.config import API_VERSION, Status
from etl.execution.exceptions import ExecutionNotAllowed


class Event(object):
    # state: State

    def __init__(self, db, path: str):
        self.db = db
        self.event_ref = db.document(path)
        self.job_ref = self.event_ref.parent.parent

        self.ID = self.event_ref.id

        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.ID}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def read_event_doc(self, transaction):
        return self.event_ref.get(transaction=transaction).to_dict()

    def read_state_doc(self, transaction):
        return self.job_ref.get(transaction=transaction).to_dict()

    # ------
    # Version
    # ------

    def set_api_version_error(self, transaction):
        transaction.update(self.event_ref, {
            'error': f'Incompatible api version found {self.api_version}, required {API_VERSION}'
        })

    def set_api_version(self, transaction):
        transaction.update(self.event_ref, {'api_version': API_VERSION})

    # ------
    # Handle
    # ------

    def set_handled(self, transaction, handled):
        transaction.update(self.event_ref, {'handled': handled})

    def handle(self):
        raise NotImplementedError

    # ------
    # Debug
    # ------

    def increase_invocation_count(self, transaction):
        transaction.update(self.event_ref, {'invocation_count': firestore_v1.transforms.Increment(1)})

    def increase_execution_count(self, transaction):
        transaction.update(self.event_ref, {'execution_count': firestore_v1.transforms.Increment(1)})


class ExecutionEvent(Event):

    def handle(self):

        @firestore_v1.transactional
        def handle_in_transaction(transaction: firestore_v1.Transaction):
            # IMPORTANT
            # Reads first

            event_dict = self.read_event_doc(transaction)
            state_dict = self.read_state_doc(transaction)

            api_version = event_dict.get('api_version', API_VERSION)
            event_handled = event_dict.get('handled', False)

            # IMPORTANT
            # Writes after

            # Check api version compatibility
            if semantic_version.Version(api_version).major != semantic_version.Version(API_VERSION).major:
                self.logger.debug('Incompatible api version')
                self.set_api_version_error(transaction)
                return

            if not event_handled:
                self.set_api_version(transaction)
                self.set_handled(transaction, True)

            old_status = state_dict.get('status', Status.NEW)
            new_status = old_status

            allow_execution = False

            if old_status in [Status.NEW, Status.WAITING_RETRY]:
                new_status = Status.RUNNING
                transaction.update(self.job_ref, {'status': new_status})
                allow_execution = True

            if old_status == Status.WAITING_SLEEP:
                new_status = Status.SLEEP
                transaction.update(self.job_ref, {'status': new_status})
                allow_execution = True

            invocation = {
                'old_status': old_status,
                'new_status': new_status,
                'allow_execution': allow_execution,
            }
            transaction.update(self.job_ref, {'invocations': firestore_v1.transforms.ArrayUnion([invocation])})

            if allow_execution:
                self.increase_execution_count(transaction)

            self.increase_invocation_count(transaction)

            self.logger.debug(invocation)

            return allow_execution

        allow_execution = handle_in_transaction(transaction=firestore_v1.Transaction(client=self.db))

        if not allow_execution:
            raise ExecutionNotAllowed


class NotifyEvent(Event):
    pass

