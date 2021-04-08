import json

from grebble_flow.grpc.generated.inner.v1.processor_pb2 import FlowExecuteResponse

from grebble_flow.grpc.generated.inner.v1 import processor_pb2_grpc
from grebble_flow.helpers.converter import grebble_converter
from grebble_flow.managment.manager import FlowManager


class ProcessorService(processor_pb2_grpc.ProcessorServicer):
    def __init__(self, *args, **kwargs):
        self.flow_manager = FlowManager()

    def Execute(self, request, context):
        # get the string from the incoming request
        flow_name = request.flowName
        content = request.content
        attributes = request.attributes

        try:
            content = json.loads(content)
        except:
            pass
        try:
            attributes = json.loads(attributes)
        except:
            pass
        for item in self.flow_manager.run(flow_name, content, attributes):
            content = json.dumps(item.content, default=grebble_converter)
            resp = FlowExecuteResponse(
                content=content.encode(),
                streamEnd=False,
                mimeType="text/plain",
                commit=True,
            )
            resp.attributes.update(item.attributes)

            yield resp

        yield FlowExecuteResponse(
            content=None, attributes=None, streamEnd=True
        )
