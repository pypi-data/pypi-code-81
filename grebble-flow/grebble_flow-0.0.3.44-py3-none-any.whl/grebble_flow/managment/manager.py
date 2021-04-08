from dataclasses_json import dataclass_json

from grebble_flow.managment.processor import find_all_processors


class FlowManager:
    def __init__(self):
        self.processor_classes = find_all_processors()

    def find_processor_instance_by_name(self, flow_name):
        result = [x for x in self.processor_classes if x.name == flow_name]
        if not result:
            raise Exception(f"Flow with name {flow_name} not found")
        if len(result) > 1:
            raise Exception(f"Multiple flow with name {flow_name}")

        return result[0]()

    def run(self, flow_name, content, attributes_req):
        flow_processor = self.find_processor_instance_by_name(flow_name)
        attributes = None
        if flow_processor.attributes:
            attributes = dataclass_json(flow_processor.attributes).from_dict(
                attributes_req
            )
        return flow_processor.execute(content=content, attributes=attributes)
