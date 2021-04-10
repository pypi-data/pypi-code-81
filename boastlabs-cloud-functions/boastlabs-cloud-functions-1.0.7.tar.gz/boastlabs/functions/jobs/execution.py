from boastlabs.functions.execution.execution import TransactionalExecutionHandler
from boastlabs.functions.execution.config import Status


class JobExecutionHandler(TransactionalExecutionHandler):

    def set_execution_state(self) -> bool:
        # -- IMPORTANT --
        # Inside a transaction reads must go before writes

        old_status = self.event.parent_data.get('status', Status.NEW)
        new_status = old_status

        allow_execution = old_status in [Status.NEW, Status.WAITING_RETRY, Status.WAITING_SLEEP]

        if old_status in [Status.NEW, Status.WAITING_RETRY]:
            new_status = Status.RUNNING
            self.transaction.update(self.event.parent_ref, {'status': new_status})

        if old_status == Status.WAITING_SLEEP:
            new_status = Status.SLEEP
            self.transaction.update(self.event.parent_ref, {'status': new_status})

        # -- DEBUGGING --

        invocation = {
            'old_status': old_status,
            'new_status': new_status,
            'allow_execution': allow_execution,
        }

        self.event.add_invocation(invocation)

        return allow_execution
