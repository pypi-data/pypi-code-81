import logging
from abc import abstractmethod

from google.cloud import firestore_v1
from google.cloud.firestore_v1 import DocumentReference

from boastlabs import __version__
from boastlabs.functions.retriable.execution.config import Status
from boastlabs.functions.retriable.execution.exceptions import ExecutionNotAllowedException, DocumentNotFoundException


class Event(object):

    def __init__(self, transaction: firestore_v1.Transaction, event_ref: DocumentReference):
        self.transaction = transaction
        self.event_ref = event_ref
        self.id = event_ref.id

        event_doc = self.event_ref.get(transaction=self.transaction)

        if not event_doc.exists:
            raise DocumentNotFoundException(doc_path=event_ref.path)

        self.data = event_doc.to_dict()

        self.event_type = self.data.get('event_type', None)
        self.api_version = self.data.get('api_version', __version__)
        self.event_handled = self.data.get('handled', False)

    def read(self):
        return self.event_ref.get(transaction=self.transaction).to_dict()

    def set_api_version(self):
        self.transaction.update(self.event_ref, {'api_version': __version__})

    def set_error(self, error):
        self.transaction.update(self.event_ref, {'error': error})

    def set_handled(self, handled):
        self.transaction.update(self.event_ref, {'handled': handled})

    def increase_invocation_count(self):
        self.transaction.update(self.event_ref, {'invocation_count': firestore_v1.transforms.Increment(1)})

    def increase_execution_count(self):
        self.transaction.update(self.event_ref, {'execution_count': firestore_v1.transforms.Increment(1)})

    def add_invocation(self, invocation):
        self.transaction.update(self.event_ref, {'invocations': firestore_v1.transforms.ArrayUnion([invocation])})


class TransactionalHandler(object):

    def __init__(self, event: Event):
        self.event = event
        self.transaction = self.event.transaction
        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.event.id}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    @abstractmethod
    def handle(self):
        raise NotImplementedError


class TriggerEventHandler(TransactionalHandler):

    def handle(self):
        # IMPORTANT
        # Reads first

        state_ref = self.event.event_ref.parent.parent
        state_dict = state_ref.get(transaction=self.transaction).to_dict()

        # IMPORTANT
        # Writes after
        old_status = state_dict.get('status', Status.NEW)
        new_status = old_status

        allow_execution = False

        if old_status in [Status.NEW, Status.WAITING_RETRY]:
            allow_execution = True
            new_status = Status.RUNNING
            self.transaction.update(state_ref, {'status': new_status})

        if old_status == Status.WAITING_SLEEP:
            allow_execution = True
            new_status = Status.SLEEP
            self.transaction.update(state_ref, {'status': new_status})

        invocation = {
            'old_status': old_status,
            'new_status': new_status,
            'allow_execution': allow_execution,
        }
        self.logger.debug(invocation)

        self.event.add_invocation(invocation)
        self.event.increase_invocation_count()
        self.transaction.update(state_ref, {'invocation_count': firestore_v1.transforms.Increment(1)})

        if allow_execution:
            self.event.increase_execution_count()
            self.transaction.update(state_ref, {'execution_count': firestore_v1.transforms.Increment(1)})
        else:
            raise ExecutionNotAllowedException(status=old_status)
