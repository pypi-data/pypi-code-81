"""
    Contains interactions with the API relating to deployed Agents.
"""
import logging
from enum import Enum
from typing import List, Dict, Union, Any
from typing_extensions import Literal

from GuardiPy.CentraObject.auxiliary_types import LabelMinimal, LabelGroupMinimal, AgentStatusFlags
from GuardiPy.CentraObject.Validation import (
    fits_schema,
    OS,
    STATUS,
    ENFORCEMENT,
    DEPLOYMENT,
    ACTIVITY,
    INSTALLED_MODULES,
    CONFIGURATION_REPORTED_ERRORS
)
from GuardiPy.helpers import CentraApiExportable, epoch_ms_to_datetime
from GuardiPy.helpers import CentraEntity


class Agent(CentraEntity):
    _path = "/agents"

    __OS = Literal[
        "Unknown",
        "Windows",
        "Linux"
    ]

    class _StatusFlags(Enum):
        POLLING_MODE = 2
        OUTDATED_POLICY = 3
        OUTDATED_CONFIGURATION = 4
        NO_REVEAL_RECEIVED = 5
        HIGH_DROP_RATE = 6
        AGENT_MISSING = 7
        PARTIAL_POLICY = 8
        ENFORCEMENT_PAUSED = 9
        NO_REVEAL_REPORTED = 10
        REVEAL_OFFLINE = 11
        ENFORCEMENT_OFFLINE = 12
        REVEAL_MODULE_ERROR = 13
        ENFORCEMENT_MODULE_ERROR = 14
        DETECTION_MODULE_ERROR = 15
        DECEPTION_MODULE_ERROR = 16
        CONTROLLER_MODULE_ERROR = 1

    __STATUS = Literal[
        "OFFLINE",
        "ONLINE"
    ]
    __ENFORCEMENT = Literal[
        "Active",
        "Not Deployed",
        "Enforcement disabled from management console"
    ]
    __DEPLOYMENT = Literal[
        "Active",
        "Not Deployed"
    ]
    __ACTIVITY = Literal[
        "last_month",
        "last_week",
        "last_12_hours",
        "last_24_hours",
        "not_active"
    ]


    @staticmethod
    def list(
            version: List[str] = None,
            kernel: List[str] = None,
            os: Union[__OS, List[__OS]] = None,  # TODO - Convert this to support any combination of. Schema Reference: OS
            labels: List[str] = None,
            label_groups: List[str] = None,  # No joke: docs say this qs param key has a space. TODO: verify.
            status: Union[__STATUS, List[__STATUS]] = None,  # Schema Reference: STATUS
            status_flags: Union[_StatusFlags, List[_StatusFlags]] = None,  # TODO - support str mapping
            module_status_enforcement: Union[__ENFORCEMENT, List[__ENFORCEMENT]] = None,  # Schema Reference: ENFORCEMENT
            module_status_deception: Union[__DEPLOYMENT, List[__DEPLOYMENT]] = None,  # Schema Reference: DEPLOYMENT
            module_status_reveal: Union[__DEPLOYMENT, List[__DEPLOYMENT]] = None,  # Schema Reference: DEPLOYMENT
            activity: Union[__ACTIVITY, List[__ACTIVITY]] = None,  # Schema Reference: ACTIVITY
            gc_filter: str = None,  # GC Docs: "Agent ID / Agent Hostname / IP Address"
            limit: int = None,
            offset: int = None,
            sort_by_property: str = None,  # Asset property to sort by
            sort_order: Literal["asc", "desc"] = "asc",  # Default sort order is ascending.
    ) -> CentraApiExportable:
        """
            GC API Docs: 'List all agents.'
        """

        payload = CentraApiExportable(path=Agent._path, method="GET", return_type=Agent,
                                      export_suffix="/export", export_view_name="agents")

        if version:
            payload.params['version'] = version
        if kernel:
            payload.params['kernel'] = kernel
        if fits_schema(os, OS):
            payload.params['os'] = os
        if labels:
            payload.params['labels'] = [label.split(':')[1] for label in labels]
        if label_groups:
            payload.params['label groups'] = label_groups
        if fits_schema(status, STATUS):
            payload.params['status'] = status
        if status_flags:
            payload.params['status_flags'] = status_flags
        if fits_schema(module_status_enforcement, ENFORCEMENT):
            payload.params['module_status_enforcement'] = module_status_enforcement
        if fits_schema(module_status_deception, DEPLOYMENT):
            payload.params['module_status_deception'] = module_status_deception
        if fits_schema(module_status_reveal, DEPLOYMENT):
            payload.params['module_status_reveal'] = module_status_reveal
        if fits_schema(activity, ACTIVITY):
            payload.params['activity'] = activity
        if gc_filter:
            payload.params['gc_filter'] = gc_filter
        if limit:
            payload.params['limit'] = limit
        if offset:
            payload.params['offset'] = offset
        if sort_by_property:  # TODO - Move these to pagination request wrapper?
            payload.params['sort'] = f"{'-' if sort_order == 'desc' else '+'}{sort_by_property}"  # ex -last_seen
        return payload

    def __init__(
            self,
            id: str = None,
            agent_id: str = None,  # UUID
            asset_id: str = None,  # UUID
            component_id: str = None,
            display_name: str = None,
            status: Literal["ONLINE", "OFFLINE"] = None,  # Schema Reference: STATUS
            build_date: int = None,
            build_commit: str = None,
            doc_version: int = None,
            first_seen: int = None,

            health: dict = None,  # TODO - Massive custom return type

            hostname: str = None,
            ip_addresses: List[str] = None,
            is_configuration_dirty: bool = None,
            is_missing: bool = None,
            is_agent_missing: bool = None,
            not_monitored: bool = None,

            labels: List[dict] = None,  # LabelMinimal
            labels_groups: List[dict] = None,  # LabelGroupMinimal

            last_seen: int = None,
            kernel: str = None,
            installed_modules: List[Literal[
                "DECEPTION_AGENT",
                "REVEAL_AGENT",
                "ENFORCEMENT_AGENT",
                "DETECTION_AGENT",
                "CONTROLLER"]] = None,  # Schema Reference: INSTALLED_MODULES
            os: Literal['UNKNOWN', 'WINDOWS', 'LINUX', 'HTTP', 'SMBLURE', 'SOLARIS'] = None,
            policy_revision: int = None,
            configuration_reported_revision: int = None,
            status_flags: List[dict] = None,
            supported_features: List[str] = None,
            version: str = None,
            configuration_reported_errors: Dict[
                Literal['enforcementagent'],
                Dict[
                    Literal['agent_dns_enable', 'agent_dns_rate_limit'],
                    str
                ]
            ] = None,  # Schema Reference: CONFIGURATION_REPORTED_ERRORS

            _id: str = None,

            # UNDOCUMENTED ADDITIONS #
            admin_lock_state: str = None,  # seen: UNLOCKED
            aggregator_component_id: str = None,  # GUID?
            configuration_override_status: str = None,  # seen: APPLIED
            configuration_updated_recently: bool = False,
            dc_inventory_revision: int = None,
            display_status: str = None,  # seen: Online
            distribution: str = None,  # seen: 'redhat 7.9'
            dns_enforcement_support: bool = None,
            full_kernel_version: str = None,  # seen: '3.10.0-1160.6.1.el7.x86_64'
            full_path_enforcement: bool = None,
            implicit_rules: List[Any] = None,
            install_date: int = None,
            kernel_config_hash: str = None,  # seen: 'efa8d986d4'
            label_groups: List[Any] = None,
            last_full_visibility_report: int = None,
            modules_supported_features: List[str] = None,  # TODO: Not mentioned in docs. RE volunteers?
            not_rules_support: bool = None,
            policy_derivation_type: int = None,
            protocol_versions: dict = None,  # TODO: Not mentioned in docs. RE volunteers?
            state: str = None,  # seen: On
            user_groups_support: bool = None,
            resource_limits: dict = None,  # TODO: Not mentioned in docs. RE volunteers?

            **kwargs
    ):
        if kwargs:
            logging.debug("Agent init: unexpected kwargs - %s", kwargs)

        self.id = id
        self.agent_id = agent_id
        self.asset_id = asset_id
        self.component_id = component_id
        self.display_name = display_name
        self.status = status if fits_schema(status, STATUS) else None
        self.build_date = epoch_ms_to_datetime(build_date)
        self.build_commit = build_commit
        self.doc_version = doc_version
        self.first_seen = epoch_ms_to_datetime(first_seen)

        self.health = health

        self.hostname = hostname
        self.ip_addresses = ip_addresses
        self.is_configuration_dirty = is_configuration_dirty
        self.is_missing = is_missing
        self.is_agent_missing = is_agent_missing
        self.not_monitored = not_monitored

        self.labels: List[LabelMinimal] = [LabelMinimal(**item) for item
                                           in (labels or [])]
        self.labels_groups: List[LabelGroupMinimal] = [LabelGroupMinimal(**item) for item
                                                       in (labels_groups or [])]

        self.last_seen = epoch_ms_to_datetime(last_seen)
        self.kernel = kernel

        self.installed_modules = []
        for module in installed_modules or []:
            if fits_schema(module, INSTALLED_MODULES):
                self.installed_modules.append(module)

        self.os = os if os in ['UNKNOWN', 'WINDOWS', 'LINUX', 'HTTP', 'SMBLURE', 'SOLARIS'] else None
        self.policy_revision = policy_revision
        self.configuration_reported_revision = configuration_reported_revision
        self.status_flags: List[AgentStatusFlags] = [AgentStatusFlags(**item) for item
                                                     in (status_flags or [])]
        self.supported_features = supported_features
        self.version = version
        self.configuration_reported_errors = configuration_reported_errors \
            if fits_schema(configuration_reported_errors, CONFIGURATION_REPORTED_ERRORS) else None

        self._id = _id

        self.admin_lock_state = admin_lock_state
        self.aggregator_component_id = aggregator_component_id
        self.configuration_override_status = configuration_override_status
        self.configuration_updated_recently = configuration_updated_recently
        self.dc_inventory_revision = dc_inventory_revision
        self.display_status = display_status
        self.distribution = distribution
        self.dns_enforcement_support = dns_enforcement_support
        self.full_kernel_version = full_kernel_version
        self.full_path_enforcement = full_path_enforcement
        self.implicit_rules = implicit_rules or []
        self.install_date = epoch_ms_to_datetime(install_date)
        self.kernel_config_hash = kernel_config_hash
        self.label_groups = label_groups or []
        self.last_full_visibility_report = epoch_ms_to_datetime(last_full_visibility_report)
        self.modules_supported_features = modules_supported_features or []
        self.not_rules_support = not_rules_support
        self.policy_derivation_type = policy_derivation_type
        self.protocol_versions = protocol_versions or {}
        self.state = state
        self.user_groups_support = user_groups_support
        self.resource_limits = resource_limits or {}
