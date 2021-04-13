import uuid


class RemoteCommand:

    def __init__(self, service_name="", method_name="", params=(), response_queue_name=""):
        self.correlation_id = str(uuid.uuid4())
        self.service_name = service_name
        self.method_name = method_name
        self.params = params
        self.response_queue_name = response_queue_name
        self.trace_id = None
        self.span_id = None
        self.result = None
        self.parent_id = None
        self.sampled = False
        self.flags = None

    def to_array(self):
        return dict(
            serviceName=self.service_name,
            methodName=self.method_name,
            params=self.params,
            responseQueueName=self.response_queue_name,
            correlationId=self.correlation_id,
            result=self.result,
            traceId=self.trace_id,
            spanId=self.span_id,
            parnetId=self.parent_id,
            sampled=self.sampled,
            flags=self.flags
        )

    def load_from_array(self, import_dict):
        self.service_name = import_dict["serviceName"]
        self.method_name = import_dict["methodName"]
        self.params = import_dict["params"]
        self.response_queue_name = import_dict["responseQueueName"]
        self.correlation_id = import_dict["correlationId"]
        self.result = import_dict["result"]
        self.trace_id = import_dict["traceId"]
        self.result = import_dict["result"]
        self.span_id = import_dict["spanId"]
        self.parent_id = import_dict["parnetId"]
        self.sampled = import_dict["sampled"]
        self.flags = import_dict["flags"]
