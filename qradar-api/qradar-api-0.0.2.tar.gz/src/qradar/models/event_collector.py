from .qradarmodel import QRadarModel


class EventCollector(QRadarModel):
    def __init__(self, *, id: int = None, name: str = None, component_name: str = None, host_id: int = None):
        self.id = id
        self.name = name
        self.component_name = component_name
        self.host_id = host_id
