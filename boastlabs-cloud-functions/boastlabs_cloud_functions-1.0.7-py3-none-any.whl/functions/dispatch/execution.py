from boastlabs.functions.execution.execution import TransactionalExecutionHandler
from boastlabs.functions.execution.config import Status


class DispatchExecutionHandler(TransactionalExecutionHandler):

    def set_execution_state(self) -> bool:
        allow_execution = not self.event.is_handled

        if allow_execution:
            self.transaction.update(self.event.parent_ref, {'status': Status.RUNNING})

        return allow_execution
