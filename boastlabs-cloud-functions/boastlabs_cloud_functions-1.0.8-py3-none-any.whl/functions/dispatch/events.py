from boastlabs.functions.execution.events.events import EventType


class DispatchStartEvent(EventType):

    def __init__(self, service_name: str, service_status: str):
        EventType.__init__(self, dict(
            event_type=EventType.DISPATCH_START,
            service_name=service_name,
            service_status=service_status))


