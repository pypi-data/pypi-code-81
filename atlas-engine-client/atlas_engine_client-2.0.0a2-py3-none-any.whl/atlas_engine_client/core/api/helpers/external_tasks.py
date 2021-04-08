from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Callable, List

from ..base_client import BaseClient
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FetchAndLockRequestPayload:
    worker_id: str
    topic_name:	str
    max_tasks:	int = 10
    long_polling_timeout: int = (10 * 1000)
    lock_duration: int = (100 * 1000)
    payload_filter: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ExternalTask:
    id: str
    worker_id: str
    topic: str
    flow_node_instance_id: str
    correlation_id: str
    process_definition_id: str
    process_instance_id: str
    owner_id: str = None
    payload: dict = None
    lock_expiration_time: str = None
    state: str = None                  # ExternalTaskStatestring(pending = pending, finished = finished)
    finished_at: str = None
    result: dict = None
    error: dict = None
    created_at: str = None

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FinishExternalTaskRequestPayload:
    worker_id: str
    result: dict

class ExternalTaskHandler(BaseClient):

    def __init__(self, url: str, identity: Callable=None):
        super(ExternalTaskHandler, self).__init__(url, identity)

    def fetch_and_lock(self, request: FetchAndLockRequestPayload, options: dict={}) -> List[ExternalTask]:
        path = '/atlas_engine/api/v1/external_tasks/fetch_and_lock'

        payload = request.to_dict()

        response_list_of_dict = self.do_post(path, payload, options)

        response = ExternalTask.schema().load(response_list_of_dict, many=True)

        return response

    def finish(self, external_task_id: str, request: FinishExternalTaskRequestPayload, options: dict={}):
        path = f"/atlas_engine/api/v1/external_tasks/{external_task_id}/finish"

        payload = request.to_dict()

        _ = self.do_put(path, payload, options)

        return True
