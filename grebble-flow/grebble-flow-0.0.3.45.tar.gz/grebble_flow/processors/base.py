from typing import Any


class FlowResponse:
    attributes: dict
    content: Any

    def __init__(self, attributes: dict, content: Any):
        self.attributes = attributes
        self.content = content


class BaseFlowProcessor(object):
    is_flow_processor = True

    def initialize(self, *args, **kwargs):
        raise NotImplemented()

    def execute(self, *args, **kwargs) -> FlowResponse:
        raise NotImplemented()
