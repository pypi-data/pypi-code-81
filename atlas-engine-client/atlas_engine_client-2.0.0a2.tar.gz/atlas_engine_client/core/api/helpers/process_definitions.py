from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from enum import IntFlag
from typing import Callable

from marshmallow.fields import Bool

from ..base_client import BaseClient

class StartCallbackType(IntFlag):
    CallbackOnProcessInstanceCreated = 1
    CallbackOnProcessInstanceFinished = 2
    CallbackOnEndEventReached = 3

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ProcessDefinitionUploadPayload:
    xml: str
    overwrite_existing: Bool = False

class ProcessDefinitionHandler(BaseClient):

    def __init__(self, url: str, identity: Callable=None):
        super(ProcessDefinitionHandler, self).__init__(url, identity)

    def deploy(self, request: ProcessDefinitionUploadPayload, options: dict={}):
        path = "/atlas_engine/api/v1/process_definitions" 

        payload = request.to_dict()

        self.do_post(path, payload, options)
