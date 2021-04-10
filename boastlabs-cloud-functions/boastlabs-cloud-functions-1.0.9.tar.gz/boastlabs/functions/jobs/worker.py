import random
import time
from abc import abstractmethod

from boastlabs.functions.execution.worker import Worker
from boastlabs.functions.execution.config import Status
from boastlabs.functions.jobs.events import JobStatusUpdateEvent


class Job(Worker):

    @abstractmethod
    def work(self):
        self.logger.debug('**** event ****')
        self.logger.debug(f'Type: {self.event.context.event_type}', )
        self.logger.debug(f'Service: {self.event.context.service_name}')
        self.logger.debug(f'Status: {self.event.context.service_status}')
        self.logger.debug('**** event ****')

        time.sleep(random.randint(0, 5))

    def set_status(self, status: str):
        # Call super
        Worker.set_status(self, status)

        # Set status of current job on dispatcher
        dispatch_ref = self.doc_ref.parent.parent
        dispatch_ref.set({
            'current_job': {
                'status': status,
                'name': self.service_name
            },
            'jobs': {
                self.service_name: {
                    'status': status
                }
            }
        }, merge=True)

        # Notify work done
        if status == Status.DONE:
            dispatch_ref.collection('events').add(
                JobStatusUpdateEvent(service_name=self.service_name, service_status=status).to_dict())
