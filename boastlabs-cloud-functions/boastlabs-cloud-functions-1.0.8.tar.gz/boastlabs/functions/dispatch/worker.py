from abc import abstractmethod

from google.cloud.firestore_v1 import DocumentReference

from boastlabs.functions.execution.config import Status
from boastlabs.functions.execution.worker import Worker
from boastlabs.functions.jobs.events import JobStartEvent


class Dispatch(Worker):
    steps: []

    @abstractmethod
    def get_steps(self):
        return ['ingest', 'transform', 'summary']

    def get_next_step(self, current_step):
        if current_step is None:
            return self.get_steps()[0]

        current_step_index = self.get_steps().index(current_step)
        if current_step_index < len(self.get_steps()) - 1:
            return self.get_steps()[current_step_index + 1]

        return None

    def trigger_next_step(self, step):
        state_ref = self.event.event_ref.parent.parent

        next_job_ref = state_ref.collection('jobs').document(step)
        next_job_ref.set({})

        next_job_ref.collection('events').add(
            JobStartEvent(service_name=step, service_status=Status.NEW).to_dict()
        )

    @abstractmethod
    def work(self):
        self.logger.debug('**** event ****')

        self.logger.debug(f'Ref: {self.event.event_ref.path }', )
        self.logger.debug(f'Type: {self.event.context.event_type}', )
        self.logger.debug(f'Service: {self.event.context.service_name}')
        self.logger.debug(f'Status: {self.event.context.service_status}')

        current_step = self.event.context.service_name
        current_status = self.event.context.service_status or Status.DONE
        next_step = self.get_next_step(current_step)

        state_ref = self.event.event_ref.parent.parent
        state_ref.update({'active': True})

        if next_step:
            if current_status == Status.DONE:
                self.trigger_next_step(next_step)
        else:
            state_ref.update({'active': False})

        self.logger.debug(f'Current Step: {current_step}')
        self.logger.debug(f'Next Step: {next_step}')

        self.logger.debug('**** event ****')
