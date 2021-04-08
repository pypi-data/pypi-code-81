from dataclasses import dataclass

from grebble_flow.processors.base import BaseFlowProcessor, FlowResponse


@dataclass
class Attributes:
    """
    Args:
       name (str): Text name description
    """
    name: str


class SimpleProcessor(BaseFlowProcessor):
    name = "simple-flow-base"
    attributes = Attributes

    def execute(self, content, attributes: Attributes, *args, **kwargs) -> FlowResponse:
        """
        :param attributes: Attributes description
        :param data: Default data description
        """

        for i in range(0, 100):
            yield FlowResponse(
                attributes={"attribute_1": "test"},
                content={"test": content, "a": attributes.name},
            )
