import json

from grebble_flow.grpc.generated.inner.v1.app_pb2 import (
    AppInfoExternalResponse,
    ProcessorExternalInfo,
    AttributeSchema,
    AttributeSchemaItem,
)
from grebble_flow.grpc.generated.inner.v1.app_pb2_grpc import ExternalAppServicer
from grebble_flow.managment.info import generate_package_info


class AppService(ExternalAppServicer):
    def __init__(self, *args, **kwargs):
        pass

    def AppInfo(self, request, context):
        info = generate_package_info()

        result = AppInfoExternalResponse()
        processors = list()
        for processor in info["processors"]:
            info = ProcessorExternalInfo(
                name=processor["name"], attributeSchema=AttributeSchema()
            )
            for key, value in processor["attributes_schema"].items():
                info.attributeSchema.items[key].CopyFrom(
                    AttributeSchemaItem(
                        type=value["type"], description=value["description"]
                    )
                )
            processors += [info]
        result.processors.extend(processors)
        return result
