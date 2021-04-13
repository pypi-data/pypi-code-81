from typing import List
from .qradarmodel import QRadarModel


class Domain(QRadarModel):

    def __init__(self, *, id: int = None, name: str = None, description: str = None, tenant_id: int = None, deleted: bool = None, event_collector_ids: List[int] = None, log_source_ids: List[int] = None,
                 log_source_group_ids: List[int] = None, custom_properties: List = None, flow_source_ids: List[int] = None, flow_collector_ids: List[int] = None, asset_scanner_ids: List[int] = None,
                 qvm_scanner_ids: List[int] = None, flow_vlans_ids: List[int] = None):

        self.id = id
        self.name = name
        self.description = description
        self.tenant_id = tenant_id
        self.deleted = deleted
        self.event_collector_ids = event_collector_ids
        self.log_source_ids = log_source_ids
        self.log_source_group_ids = log_source_group_ids
        self.custom_properties = custom_properties
        self.flow_source_ids = flow_source_ids
        self.flow_collector_ids = flow_collector_ids
        self.asset_scanner_ids = asset_scanner_ids
        self.qvm_scanner_ids = qvm_scanner_ids
        self.flow_vlans_ids = flow_vlans_ids
