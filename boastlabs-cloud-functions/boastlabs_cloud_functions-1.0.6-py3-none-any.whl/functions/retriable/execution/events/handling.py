import logging
import semantic_version

from google.cloud import firestore_v1
from google.cloud.firestore_v1 import DocumentReference

from boastlabs import __version__
from boastlabs.functions.retriable.execution.exceptions import (
    ExecutionNotAllowedException,
    HandlerNotFoundException,
    IncompatibleApiVersionException,
    RetryException)
from boastlabs.functions.retriable.execution.events.handler import Event, TriggerEventHandler
from boastlabs.functions.retriable.execution.config import Status


MAX_ATTEMPTS = 50


class EventHandling(object):

    def __init__(self, db, event_ref: DocumentReference):
        self.db = db
        self.event_ref = event_ref

        self.handlers = {}

        self.register_handler('trigger', TriggerEventHandler)

    def register_handler(self, event_type, handler):
        self.handlers[event_type] = handler

    def get_handler(self, event_type):
        return self.handlers.get(event_type, None)

    def handle(self):

        @firestore_v1.transactional
        def handle_in_transaction(transaction: firestore_v1.Transaction):
            # IMPORTANT
            # Read operations must be first

            event = Event(event_ref=self.event_ref, transaction=transaction)

            # Check api version compatibility
            if semantic_version.Version(event.api_version).major == semantic_version.Version(__version__).major:
                handler_class = self.get_handler(event.event_type)
                if handler_class:
                    handler = handler_class(event=event)
                    handler.handle()
                    event.set_api_version()
                    event.set_handled(True)
                else:
                    raise HandlerNotFoundException(event_type=event.event_type,
                                                   known_events=[e for e in self.handlers])
            else:
                raise IncompatibleApiVersionException(found_api_version=event.set_api_version(),
                                                      current_api_version=__version__)
        try:
            handle_in_transaction(transaction=firestore_v1.Transaction(client=self.db, max_attempts=MAX_ATTEMPTS))
        except ExecutionNotAllowedException as e:
            raise e
        except HandlerNotFoundException as e:
            raise e
        except IncompatibleApiVersionException as e:
            raise e
        except Exception:
            raise RetryException


class EventWorkDone(object):

    def __init__(self, db):
        self.db = db
        self.logger = self._init_logger()

    def _init_logger(self):
        logger = logging.getLogger(f"[{self.__class__.__name__}]")
        logger.setLevel(logging.DEBUG)

        stdout = logging.StreamHandler()
        logger.addHandler(stdout)

        stdout.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s'))
        return logger

    def create(self,
               job_ref: DocumentReference,
               parent_ref: DocumentReference,
               service_name: str,
               service_status: str):

        @firestore_v1.transactional
        def handle_in_transaction(transaction: firestore_v1.Transaction):
            transaction.update(job_ref, {'active': False, 'status': Status.DONE})
            transaction.update(parent_ref, {'status': Status.DONE})

            event_ref = parent_ref.collection('events').document()

            transaction.set(event_ref, {
                'service_name': service_name,
                'service_status': service_status,
                'event_type': 'trigger'
            })

        handle_in_transaction(transaction=firestore_v1.Transaction(client=self.db, max_attempts=MAX_ATTEMPTS))
