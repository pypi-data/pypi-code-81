from abc import abstractmethod

from google.cloud import firestore_v1

from boastlabs.functions.execution.events.events import Event


class TransactionalExecutionHandler(object):

    def __init__(self, transaction: firestore_v1.Transaction, event: Event):
        self.transaction = transaction
        self.event = event

    @abstractmethod
    def set_execution_state(self) -> bool:
        raise NotImplementedError
