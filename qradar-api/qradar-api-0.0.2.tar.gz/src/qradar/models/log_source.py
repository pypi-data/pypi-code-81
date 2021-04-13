from typing import List
from .qradarmodel import QRadarModel


class Logsource(QRadarModel):

    def __init__(self, *, id: int = None, name: str = None, description: str = None, type_id: int = None, protocol_type_id: int = None, protocol_parameters: List = None, enabled: bool = None, gateway: str = None,
                 internal: bool = None, credibility: int = None, target_event_collector_id: int = None, disconnected_log_collector_id: int = None, coalesce_events: bool = None, store_event_payload: bool = None,
                 log_source_extension_id: int = None, language_id: int = None, group_ids: List[int] = None, requires_deploy: bool = None, status: str = None, auto_discovered: bool = None, average_eps: int = None,
                 creation_date: str = None, modified_date: str = None, last_event_time: str = None, wincollect_internal_destination_id: int = None,
                 wincollect_external_destination_ids: List[int] = None, legacy_bulk_group_name: str = None, sending_ip: str = None, parsing_order: int = None):

        self.id = id
        self.name = name
        self.description = description
        self.type_id = type_id
        self.protocol_type_id = protocol_type_id
        self.protocol_parameters = protocol_parameters
        self.enabled = enabled
        self.gateway = gateway
        self.internal = internal
        self.credibility = credibility
        self.target_event_collector_id = target_event_collector_id
        self.disconnected_log_collector_id = disconnected_log_collector_id
        self.coalesce_events = coalesce_events
        self.store_event_payload = store_event_payload
        self.log_source_extension_id = log_source_extension_id
        self.language_id = language_id
        self.group_ids = group_ids
        self.requires_deploy = requires_deploy
        self.status = status
        self.auto_discovered = auto_discovered
        self.average_eps = average_eps
        self.creation_date = creation_date
        self.modified_date = modified_date
        self.last_event_time = last_event_time
        self.wincollect_internal_destination_id = wincollect_internal_destination_id
        self.wincollect_external_destination_ids = wincollect_external_destination_ids
        self.legacy_bulk_group_name = legacy_bulk_group_name
        self.sending_ip = sending_ip
        self.parsing_order = parsing_order
