from datetime import date
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase, Undefined
from typing import Any, Callable, List
from urllib.parse import urlencode

from ..base_client import BaseClient

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ProcessInstanceQueryRequest:
    offset: int = 0
    limit: int = -1
    correlation_id: str = None
    process_instance_id: str = None
    process_definition_id: str = None
    process_model_id: str = None
    process_model_name: str = None
    process_model_hash: str = None
    owner_id: str = None
    state: str = None
    parent_process_instance_id: str = None
    terminated_by_user_id: str = None
    created_before: date = None
    created_at: date = None
    created_after: date = None
    updated_before: date = None
    updated_at: date = None
    updated_after: date = None
    finished_before: date = None
    finished_at: date = None
    finished_after: date = None
    start_token: dict = None
    end_token: dict = None
@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class ProcessInstanceQueryResponse:
    correlation_id: str = None
    process_instance_id: str = None
    process_definition_id: str = None
    process_model_id: str = None
    process_model_name: str = None
    parent_process_instance_id: str = None
    hash: str = None
    xml: str = None
    state: str = None
    error: dict = None
    owner_id: str = None
    created_at: str = None
    finished_at: str = None
    terminated_by_user_id: str = None
    start_token: str = None
    end_token: str = None
    metadata: dict = None
    #correlation: Any = None

class ProcessInstanceHandler(BaseClient):

    def __init__(self, url: str, identity: Callable=None):
        super(ProcessInstanceHandler, self).__init__(url, identity)

    def query(self, request: ProcessInstanceQueryRequest, options: dict={}) -> List[ProcessInstanceQueryResponse]:
        path = "/atlas_engine/api/v1/process_instances/query"

        all_fields = request.to_dict()

        query_fields = [(key, value) for key, value in all_fields.items() if value is not None]

        query = urlencode(query_fields)

        if len(query) > 0:
            path = f"{path}?{query}"

        response_list_of_dict = self.do_get(path, options)

        if response_list_of_dict.get('totalCount', 0) > 0:
            json_data = response_list_of_dict['processInstances']
            response = ProcessInstanceQueryResponse.schema().load(json_data, many=True)
        else:
            response = []

        return response


    def terminate(self, process_instance_id: str, options: dict={}):
        path = f"/atlas_engine/api/v1/process_instances/{process_instance_id}/terminate"

        _ = self.do_put(path, {}, options)

        return True
