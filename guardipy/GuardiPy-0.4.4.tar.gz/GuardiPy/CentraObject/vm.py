"""
    Event type definitions pulled from GC API docs - Schema/VM section.
    Includes NIC as well; seems related...
"""
import logging
from typing import List
from GuardiPy.CentraObject.auxiliary_types import OrchestrationDetail
from GuardiPy.helpers import CentraEntity


class NIC(CentraEntity):
    """ No docs in API regarding this type. """

    def __repr__(self):
        return f"NIC {('on VLAN:' + str(self.vlan_id)) or ''} ({self.network_id})"

    def __init__(
            self,
            discovered_ip_addresses: List[str] = None,
            ip_addresses: List[str] = None,
            mac_address: str = None,
            network_id: str = None,
            network_name: str = None,
            network_orchestration_id: str = None,
            orchestration_details: List[dict] = None,
            switch_id: str = None,
            vif_id: str = None,
            vlan_id: int = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"NIC init: unexpected kwargs:  {kwargs}")
        self.discovered_ip_addresses: List[str] = discovered_ip_addresses or []
        self.ip_addresses: List[str] = ip_addresses or []
        self.mac_address = mac_address
        self.network_id = network_id
        self.network_name = network_name
        self.network_orchestration_id = network_orchestration_id
        self.orchestration_details: List[OrchestrationDetail] = [OrchestrationDetail(**item) for item in
                                                                 (orchestration_details or [])]
        self.switch_id = switch_id
        self.vif_id = vif_id
        self.vlan_id = vlan_id


class VM(CentraEntity):
    """ No docs in API regarding this type. """

    def __repr__(self):
        return f"VM '{self.name}' ({self.id})"

    def __init__(
            self,
            full_name: str = None,
            id: str = None,
            name: str = None,
            nics: List[dict] = None,
            orchestration_details: List[dict] = None,
            recent_domains: List[str] = None,
            tenant_name: str = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"VM init: unexpected kwargs:  {kwargs}")
        self.full_name = full_name
        self.id = id
        self.name = name
        self.nics: List[NIC] = [NIC(**item) for item
                                in (nics or [])]
        self.orchestration_details: List[OrchestrationDetail] = [OrchestrationDetail(**item) for item in
                                                                 (orchestration_details or [])]
        self.recent_domains: List[str] = recent_domains or []
        self.tenant_name = tenant_name
