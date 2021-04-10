import logging
import semantic_version

from google.cloud import firestore_v1
from google.cloud.firestore_v1 import DocumentReference

from boastlabs import __version__
from boastlabs.functions.execution.exceptions import (
    DocumentNotFoundException,
    IncompatibleApiVersionException,
    ExecutionNotAllowedException,
    HandlerNotFoundException,
    RetryException)

from boastlabs.functions.execution.events.events import Event, EventType
from boastlabs.functions.jobs.execution import JobExecutionHandler
from boastlabs.functions.dispatch.execution import DispatchExecutionHandler


class EventHandler(object):
    def __init__(self, db, event_ref: DocumentReference):
        self.db = db
        self.event_ref = event_ref
        self.parent_ref = event_ref.parent.parent
        self.logger = self._init_logger()

        self.event_types = [EventType.DISPATCH_START, EventType.JOB_START, EventType.JOB_STATUS_UPDATE]

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.event_ref.id}] [{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def create_event(self, event_data: dict, parent_data: dict) -> Event:
        event = Event(event_data=event_data, parent_data=parent_data, event_ref=self.event_ref)
        try:
            if event.context.event_type not in self.event_types:
                raise HandlerNotFoundException(event_type=event.context.event_type)
            if event.context.api_version:
                found_version = semantic_version.Version(event.context.api_version)
                current_version = semantic_version.Version(__version__)

                if found_version.major != current_version.major:
                    raise IncompatibleApiVersionException(found_api_version=event.context.api_version,
                                                          current_api_version=__version__)
        except Exception as e:
            event.error = str(e)
        finally:
            return event

    def set_event_handled(self, transaction, event):
        event.is_handled = True
        transaction.update(self.event_ref, event.to_dict())

    def _handle(self):

        @firestore_v1.transactional
        def handle_in_transaction(transaction: firestore_v1.Transaction):
            event_doc = self.event_ref.get(transaction=transaction)
            parent_doc = self.parent_ref.get(transaction=transaction)

            if not event_doc.exists:
                raise DocumentNotFoundException(doc_path=self.event_ref.path)

            event = self.create_event(event_data=event_doc.to_dict(), parent_data=parent_doc.to_dict())

            if event.error:
                event.allow_execution = False
                self.set_event_handled(transaction=transaction, event=event)
                return event

            if event.context.event_type in [EventType.DISPATCH_START, EventType.JOB_STATUS_UPDATE]:
                handler = DispatchExecutionHandler(transaction=transaction, event=event)
                event.allow_execution = handler.set_execution_state()

            if event.context.event_type in [EventType.JOB_START]:

                handler = JobExecutionHandler(transaction=transaction, event=event)
                event.allow_execution = handler.set_execution_state()

            self.set_event_handled(transaction=transaction, event=event)

            return event

        return handle_in_transaction(transaction=firestore_v1.Transaction(client=self.db))

    def handle(self):
        try:
            event = self._handle()
            if not event.allow_execution:
                raise ExecutionNotAllowedException()
            return event
        except ExecutionNotAllowedException:
            raise
        except Exception as e:
            raise RetryException
