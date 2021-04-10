from firebase_admin import firestore
from google.cloud import firestore_v1
from google.cloud.firestore_v1 import DocumentReference

from boastlabs import __version__


class EventType:
    JOB_STATUS_UPDATE = 'job_status_update'
    JOB_START = 'job_start'
    DISPATCH_START = 'dispatch_start'

    api_version: str
    event_type: str
    service_name: str
    service_status: str

    def __init__(self, data: dict):
        self.api_version = data.get('api_version', None)
        self.event_type = data.get('event_type', None)
        self.service_name = data.get('service_name', None)
        self.service_status = data.get('service_status', None)

    def to_dict(self):
        return {
            'context': {
                'api_version': __version__,
                'event_type': self.event_type,
                'service_name': self.service_name,
                'service_status': self.service_status,
                'created_at': firestore.SERVER_TIMESTAMP
            }
        }


class Event(object):

    context: EventType

    id: str
    is_handled: bool
    error: str
    error: None
    invocations: []
    allow_execution: bool

    def __init__(self, event_data: dict, parent_data: dict, event_ref: DocumentReference):
        self.event_data = event_data
        self.event_ref = event_ref

        # TODO
        self.parent_data = parent_data
        self.parent_ref = event_ref.parent.parent

        self.context = EventType(event_data.get('context', {}))

        self.allow_execution = False
        self.error = event_data.get('error', None)
        self.invocations = event_data.get('invocations', [])
        self.is_handled = event_data.get('handled', False)

    def to_dict(self):
        return {
            'handled': self.is_handled,
            'handling': {
                'api_version': __version__,
                'error': self.error,
            },
            'invocation_count': firestore_v1.transforms.Increment(1),
            'execution_count': firestore_v1.transforms.Increment(1 if self.allow_execution else 0),
            'invocations': self.invocations,
        }

    def add_invocation(self, invocation):
        self.invocations += [invocation]


