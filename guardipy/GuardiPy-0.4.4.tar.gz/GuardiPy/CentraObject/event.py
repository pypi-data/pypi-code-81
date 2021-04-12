"""
    Event type definitions pulled from GC API docs - Schema/Event section.
"""
import logging
from typing import List
from typing_extensions import Literal
from GuardiPy.helpers import CentraEntity
from GuardiPy.CentraObject.Validation import fits_schema, EVENT_TYPE


class Event(CentraEntity):
    """ Querying methods TBD... """

    def __repr__(self):
        return f"{self.severity} Event ({self.id})"

    def __init__(
            self,
            description: str = None,
            destinations: List[List[str]] = None,
            doc_version: int = None,
            event_source: str = None,
            event_type: Literal["DatapathRedirectEvent", "HoneypotRedirectEvent", "HoneypotSecurityEvent",
                                "HoneypotSecurityNetworkEvent", "SystemEvent", "DatapathScanDetectionEvent",
                                "DatapathCrashEvent", "HoneypotSystemEvent"] = None,  # Schema Reference: EVENT_TYPE
            id: str = None,
            incident_id: str = None,
            is_experimental: bool = None,
            processed_time: int = None,
            received_time: int = None,
            severity: int = None,
            source_ip: str = None,
            source_vm: dict = None,
            tag_refs: List[str] = None,
            time: int = None,
            uuid: str = None,
            _id: str = None,

            ### UNDCOUMENTED ADDITIONS ###

            service: str = None,  # Example: 'Unknown'
            os: str = None,  # Example: 'Windows'
            service_provider_id: str = None,  # Example: '160489a2-2362-48cd-8d1d-6082f6274110'
            direction: str = None,  # Example: 'Incoming'
            source_mac: str = None,  # Example: '00:01:02:03:04:05'
            destination_mac: str = None,  # Example: '00:0C:29:CF:12:4E'
            destination_ip: str = None,  # Example: '10.5.5.21'
            source_port: int = None,
            destination_port: int = None,
            event_group: str = None,  # Example: 'Network'
            type: str = None,  # Example: 'ConnectAttempt'
            visibility: str = None,  # Example: 'Front'

            **kwargs
    ):
        if kwargs:
            logging.debug(f"Event init: unexpected kwargs?:  {kwargs}")

        self.description = description
        self.destinations: List[List[str]] = destinations or []
        self.doc_version = doc_version
        self.event_source = event_source
        self.event_type = event_type if fits_schema(event_type, EVENT_TYPE) else None
        self.id = id
        self.incident_id = incident_id
        self.is_experimental = is_experimental
        self.processed_time = processed_time
        self.received_time = received_time
        self.severity = severity
        self.source_ip = source_ip
        self.source_vm = source_vm
        self.tag_refs: List[str] = tag_refs or []
        self.time = time
        self.uuid = uuid
        self._id = _id

        self.service = service,
        self.os = os,
        self.service_provider_id = service_provider_id,
        self.direction = direction,
        self.source_mac = source_mac,
        self.destination_mac = destination_mac,
        self.destination_ip = destination_ip,

        self.source_port = source_port
        self.destination_port = destination_port
        self.event_group = event_group
        self.type = type
        self.visibility = visibility
