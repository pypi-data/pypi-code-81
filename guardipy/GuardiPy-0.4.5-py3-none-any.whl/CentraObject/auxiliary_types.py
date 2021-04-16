"""
    Contains type definitions for items that are denoted as an 'Object' (inline!) in the API docs.
    That is - objects which are not given their own 'sections' in the Schema area of the API official API docs.
    In some areas I may put these in other CentraObject.* modules. Such as "NIC" being under "VM."
    Rule of thumb: nothing in here should be a complex type. """
import logging
from typing import List, Optional
from typing_extensions import Literal

from GuardiPy.CentraObject.Validation import (
    fits_schema,
    ASSET_TYPE,
    RECOMMENDATION_TYPE,
    HANDLE_TEMPLATE,
    RULE_TYPE,
    FLAG_TYPE
)
from GuardiPy.helpers import CentraEntity, CentraApiPayload


class ConcatenatedTag(CentraEntity):
    def __repr__(self):
        return f"Tag '{self.display_name}' ({self.tag_class})"

    def __init__(
            self,
            display_name: str,
            tag_class: str,

            # UNDOCUMENTED ADDITIONS #
            events: List[str] = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"ConcatenatedTag init: unexpected kwargs?:  {kwargs}")
        self.display_name = display_name
        self.tag_class = tag_class

        self.events = events


class NetworkDestination:
    def __repr__(self):
        return f"NetworkDestination IP:{self.ip_int} ({len(self.ports)} ports)"

    def __init__(
            self,
            ip_int: int = None,  # int64, TODO - look into this. is bit-mapping an IP addr to an int?...  foreign key..?
            ports: List[str] = None,  # Not limited to integers like TCP/UDP port nums, can also be "ARP" for example...
            **kwargs
    ):
        if kwargs:
            logging.debug(f"NetworkDestination init: unexpected kwargs?:  {kwargs}")
        self.ip_int = ip_int
        self.ports: List[str] = ports or []


class BareMinimumAsset(CentraEntity):
    def __repr__(self):
        return f"BareMinimumAsset {self.asset_type} @ {self.asset_id}"

    def __init__(
            self,
            asset_id: str = None,
            asset_type: Literal["IP", "VM"] = None,  # Schema Reference: ASSET_TYPE
            **kwargs
    ):
        if kwargs:
            logging.debug(f"BareMinimumAsset init: unexpected kwargs?:  {kwargs}")
        self.asset_id = asset_id
        self.asset_type = asset_type if fits_schema(asset_type, ASSET_TYPE) else None


class IncidentGroup(CentraEntity):
    def __repr__(self):
        return f"IncidentGroup {self.gname} ({self.gid})"

    def __init__(
            self,
            gid: str = None,
            gname: str = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"IncidentGroup init: unexpected kwargs?:  {kwargs}")
        self.gid = gid
        self.gname = gname


class IOC(CentraEntity):
    def __repr__(self):
        return f"IOC from {self.source} ({len(self.initiating_tags)} tags) ({self.ioc_id})"

    def __init__(
            self,
            initiating_tags: List[str] = None,
            ioc_id: str = None,
            source: str = None,
            related_tags: List[str] = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"IOC init: unexpected kwargs?:  {kwargs}")
        self.initiating_tags: Optional[List[str]] = initiating_tags
        self.ioc_id = ioc_id
        self.source = source
        self.related_tags: Optional[List[str]] = related_tags


class RecommendationPart(CentraEntity):
    def __repr__(self):
        return f"{self.type} RecommendationPart {self.value}"

    def __init__(
            self,
            type: Literal["text", "expression", "mute", "bold"],  # Schema Reference: RECOMMENDATION_TYPE
            value: str,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"RecommendationPart init: unexpected kwargs:  {kwargs}")
        self.type = type if fits_schema(type, RECOMMENDATION_TYPE) else None
        self.value = value


class Recommendation(CentraEntity):
    def __repr__(self):
        return f"{self.rule_type} Recommendation ({self.id})"

    def __init__(
            self,
            id: str = None,
            parts: List[dict] = None,
            handle_template: Literal[
                "VMRecommendation", "NetworkVMRecommendation", "FileQuarantineRecommendation",
                "RansomwareVMRecommendation", "RansomwareNonVMRecommendation", "PanIpRecommendation"
            ] = None,  # Schema Reference: HANDLE_TEMPLATE
            rule_id: str = None,
            rule_type: Literal["FILES", "NETWORK"] = None,  # Schema Reference: RULE_TYPE
            **kwargs
    ):
        if kwargs:
            logging.debug(f"Recommendation init: unexpected kwargs:  {kwargs}")
        self.id = id
        self.parts: List[RecommendationPart] = [RecommendationPart(**item) for item in
                                                (parts or [])]
        self.handle_template = handle_template if fits_schema(handle_template, HANDLE_TEMPLATE) else None
        self.rule_id = rule_id
        self.rule_type = rule_type if fits_schema(rule_type, RULE_TYPE) else None


class OrchestrationDetail(CentraEntity):
    def __repr__(self):
        return f"{self.orchestration_type} OrchestrationDetail: {self.orchestration_id}"

    def __init__(
            self,
            orchestration_id: str = None,
            orchestration_type: str = None,
            orchestration_obj_id: str = None,
            revision_id: int = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"RecommendationPart init: unexpected kwargs:  {kwargs}")
        self.orchestration_id = orchestration_id
        self.orchestration_type = orchestration_type
        self.orchestration_obj_id = orchestration_obj_id
        self.revision_id = revision_id


class LabelMinimal(CentraEntity):
    def __str__(self):
        return f'labels:{self.id}'

    def __repr__(self):
        return f'MinimalLabel<{self.id}> "{self.key}": {self.value}'

    @staticmethod
    def list(
            assets: str = None,
            find_matches: bool = None,
            dynamic_criteria_limit: int = None,
            key: str = None,
            value: str = None,
            limit: int = None,
            offset: int = 0
    ) -> CentraApiPayload:
        params = {}
        if assets:
            params['assets'] = assets
        if find_matches:
            params['find_matches'] = find_matches
        if dynamic_criteria_limit:
            params['dynamic_criteria_limit'] = dynamic_criteria_limit
        if key:
            params['key'] = key
        if value:
            params['value'] = value
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        payload = CentraApiPayload(
            path="/visibility/labels", method="GET", return_type=LabelMinimal,
            params=params, response_pagination=True
        )
        return payload

    def __init__(
            self,
            id: str = None,  # UUID of label
            key: str = None,
            value: str = None,
            name: str = None,

            # UNDOCUMENTED ADDITIONS #
            color_index: int = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"LabelMinimal init: unexpected kwargs?:  {kwargs}")
        self.id = id
        self.key = key
        self.value = value
        self.name = name


class LabelGroupMinimal(CentraEntity):  # Same as LabelMinimal but just being semantic, here...
    def __repr__(self):
        return f'LabelGroupMinimal<{self.name}> "{self.key}": {self.value}'

    def __init__(
            self,
            id: str = None,  # UUID of label
            key: str = None,
            value: str = None,
            name: str = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"LabelGroupMinimal init: unexpected kwargs?:  {kwargs}")
        self.id = id
        self.key = key
        self.value = value
        self.name = name


class AgentStatusFlags(CentraEntity):
    def __repr__(self):
        return f'AgentStatusFlags: {self.flag_type}'

    def __init__(
            self,
            flag_type: Literal[
                'PollingMode',
                'OutdatedPolicy',
                'OutdatedConfiguration',
                'NoRevealReceived',
                'HighDropRate',
                'AgentMissing',
                'PartialPolicy',
                'EnforcementPaused',
                'NoRevealReported',
                'RevealOffline',
                'EnforcementOffline',
                'RevealModuleError',
                'EnforcementModuleError',
                'DetectionModuleError',
                'DeceptionModuleError',
                'ControllerModuleError'
            ] = None,  # Schema Reference: FLAG_TYPE
            last_seen_time: bool = None,  # ??? supposed to be int?? indicates it updated the agent's last_seen_time???
            **kwargs
    ):
        if kwargs:
            logging.debug(f"LabelGroupMinimal init: unexpected kwargs?:  {kwargs}")
        self.flag_type = flag_type if fits_schema(flag_type, FLAG_TYPE) else None
        self.last_seen_time = last_seen_time
