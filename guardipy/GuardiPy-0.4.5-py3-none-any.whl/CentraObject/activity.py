"""
    Contains interactions with the API relating to Network Activity.
"""
import logging
from datetime import datetime, timedelta
from typing import Union, TypeVar, List, Dict

from typing_extensions import Literal

from GuardiPy.helpers import CentraApiExportable
from GuardiPy.helpers import CentraEntity

CONNECTION_TYPE = TypeVar(
    name="CONNECTION_TYPE",
    bound=Literal["successful", "failed", "redirected_to_hpvm"]
)
POLICY_VERDICT = TypeVar(
    name="POLICY_VERDICT",
    bound=Literal["blocked", "will_be_blocked", "alerted_by_management", "blocked_by_management", "allowed"]
)


class LabelsLog(CentraEntity):
    __path = "/labels-log"

    def __repr__(self):
        return f"Labels Log: asset_ip: {self.asset_ip}, ip_addresses: {self.ip_addresses}"

    @staticmethod
    def list(
            from_time: Union[datetime, timedelta, int, str] = timedelta(days=-1),  # REQUIRED: Incident search range.
            to_time: Union[datetime, timedelta, int, str] = datetime.utcnow(),  # REQUIRED: Incident search range
            all_labels: Union[str, List[str]] = None,
            asset_name: Union[str, List[str]] = None,
            change_cause: Union[str, List[str]] = None,
            changed_by: Union[str, List[str]] = None,
            changed_by_type: Union[str, List[str]] = None,
            changed_labels: Union[str, List[str]] = None,
    ) -> CentraApiExportable:
        payload = CentraApiExportable(
            path=LabelsLog.__path, method="GET", return_type=LabelsLog,
            export_suffix='/export', export_view_name="labels-log",
            params={"from_time": from_time, "to_time": to_time}
        )
        if all_labels:
            payload.params.update({"all_labels": all_labels})
        if asset_name:
            payload.params.update({"asset_name": asset_name})
        if change_cause:
            payload.params.update({"change_cause": change_cause})
        if changed_by:
            payload.params.update({"changed_by": changed_by})
        if changed_by_type:
            payload.params.update({"changed_by_type": changed_by_type})
        if changed_labels:
            payload.params.update({"changed_labels": changed_labels})
        return payload

    def __init__(
            self,
            asset_ip: str = None,
            all_labels: Dict = None,
            asset: str = None,
            asset_id: str = None,
            asset_ips: Dict = None,
            asset_name: str = None,
            change_cause: str = None,
            changed_by: Dict = None,
            changed_labels: Dict = None,
            id: str = None,
            ip_addresses: Dict = None,
            label_groups: Dict = None,
            name: str = None,
            report_time: int = None,
            **kwargs
    ):
        self.asset_ip = asset_ip
        self.all_labels = all_labels
        self.asset = asset
        self.asset_id = asset_id
        self.asset_ips = asset_ips
        self.asset_name = asset_name
        self.change_cause = change_cause
        self.changed_by = changed_by
        self.changed_labels = changed_labels
        self.id = id
        self.ip_addresses = ip_addresses
        self.label_groups = label_groups
        self.name = name
        self.report_time = report_time
        if kwargs:
            logging.debug("Labels init: unexpected kwargs - %s", kwargs)


class NetworkLog(CentraEntity):
    __path = "/connections"

    def __repr__(self):
        return f"Network Log: src: {self.source_ip}, dst: {self.destination_ip}"

    @staticmethod
    def list(
            any_side: Union[str, List[str]] = None,
            connection_type: Union[CONNECTION_TYPE, List[CONNECTION_TYPE]] = None,
            destination: Union[str, List[str]] = None,
            from_time: Union[datetime, timedelta, int, str] = timedelta(days=-1),  # REQUIRED: Incident search range.
            has_mismatch_alert: bool = None,
            policy_ruleset: Union[str, List[str]] = None,
            policy_verdict: Union[POLICY_VERDICT, List[POLICY_VERDICT]] = None,
            port: Union[int, List[int]] = None,
            protocols: Union[Literal["TCP", "UDP"], List[Literal["TCP", "UDP"]]] = None,
            source: Union[str, List[str]] = None,
            to_time: Union[datetime, timedelta, int, str] = datetime.utcnow(),  # REQUIRED: Incident search range
    ) -> CentraApiExportable:
        """
            List all Activity.  -GC Docs
            from_time and to_time are required - timezones are in UTC Epoch Milliseconds.
        """

        assert from_time  # Check for missing required parameter (per API docs)
        assert to_time  # Check for missing required parameter (per API docs)

        payload = CentraApiExportable(
            path=NetworkLog.__path, method="GET", return_type=NetworkLog,
            export_suffix='/export', export_view_name="network-log",
            params={"from_time": from_time, "to_time": to_time}
        )

        if any_side:
            payload.params.update({"any_side": any_side})
        if destination:
            payload.params.update({"destination": destination})
        if connection_type:
            payload.params.update({"connection_type": connection_type})
        if has_mismatch_alert:
            payload.params.update({"has_mismatch_alert": has_mismatch_alert})
        if policy_ruleset:
            payload.params.update({"policy_ruleset": policy_ruleset})
        if policy_verdict:
            payload.params.update({"policy_verdict": policy_verdict})
        if port:
            payload.params.update({"port": port})
        if protocols:
            payload.params.update({"protocols": protocols})
        if source:
            payload.params.update({"source": source})

        return payload

    def __init__(
            self,
            bucket_id: str = None,
            connection_type: CONNECTION_TYPE = None,
            count: int = None,
            db_insert_time: int = None,
            destination: object = None,
            destination_asset_hash: int = None,
            destination_ip: str = None,
            destination_node_id: str = None,
            destination_node_type: str = None,
            destination_port: int = None,
            destination_process: str = None,
            destination_full_path: str = None,
            destination_process_id: str = None,
            destination_process_name: str = None,
            destination_username: str = None,
            flow_id: str = None,
            has_mismatch_alert: bool = None,
            id: str = None,
            incidents: bool = None,
            ip_protocol: str = None,
            original_policy_verdict: POLICY_VERDICT = None,
            policy_rule: str = None,
            policy_ruleset: str = None,
            policy_section: str = None,
            policy_verdict: POLICY_VERDICT = None,
            slot_start_time: int = None,
            source: object = None,
            source_asset_hash: int = None,
            source_ip: str = None,
            source_node_id: str = None,
            source_node_type: str = None,
            source_process: str = None,
            source_process_full_path: str = None,
            source_process_id: str = None,
            source_process_name: str = None,
            source_username: str = None,
            violates_policy: bool = None,
            **kwargs
    ):

        self.bucket_id = bucket_id
        self.connection_type = connection_type
        self.count = count
        self.db_insert_time = db_insert_time
        self.destination = destination
        self.destination_asset_hash = destination_asset_hash
        self.destination_ip = destination_ip
        self.destination_node_id = destination_node_id
        self.destination_node_type = destination_node_type
        self.destination_port = destination_port
        self.destination_process = destination_process
        self.destination_full_path = destination_full_path
        self.destination_process_id = destination_process_id
        self.destination_process_name = destination_process_name
        self.destination_username = destination_username
        self.flow_id = flow_id
        self.has_mismatch_alert = has_mismatch_alert
        self.id = id
        self.incidents = incidents
        self.ip_protocol = ip_protocol
        self.original_policy_verdict = original_policy_verdict
        self.policy_rule = policy_rule
        self.policy_ruleset = policy_ruleset
        self.policy_section = policy_section
        self.policy_verdict = policy_verdict
        self.slot_start_time = slot_start_time
        self.source = source
        self.source_asset_hash = source_asset_hash
        self.source_ip = source_ip
        self.source_node_id = source_node_id
        self.source_node_type = source_node_type
        self.source_process = source_process
        self.source_process_full_path = source_process_full_path
        self.source_process_id = source_process_id
        self.source_process_name = source_process_name
        self.source_username = source_username
        self.violates_policy = violates_policy
        if kwargs:
            logging.debug("NetworkLog init: unexpected kwargs - %s", kwargs)


class RedirectionsLog(CentraEntity):
    __path = "/redirection-events"

    def __repr__(self):
        return f"Redirections Log: src: {self.source_ip}, dst: {self.destination_ip}"

    @staticmethod
    def list(
            destination: Union[str, List[str]] = None,
            from_time: Union[datetime, timedelta, int, str] = timedelta(days=-1),  # REQUIRED: Incident search range.
            port: Union[int, List[int]] = None,
            source: Union[str, List[str]] = None,
            to_time: Union[datetime, timedelta, int, str] = datetime.utcnow(),  # REQUIRED: Incident search range
    ) -> CentraApiExportable:
        """
            List all Activity.  -GC Docs
            from_time and to_time are required - timezones are in UTC Epoch Milliseconds.
        """

        assert from_time  # Check for missing required parameter (per API docs)
        assert to_time  # Check for missing required parameter (per API docs)

        payload = CentraApiExportable(
            path=RedirectionsLog.__path, method="GET", return_type=RedirectionsLog,
            export_suffix='/export', export_view_name="redirections-log",
            params={"from_time": from_time, "to_time": to_time}
        )
        if destination:
            payload.params.update({"destination": destination})
        if port:
            payload.params.update({"port": port})
        if source:
            payload.params.update({"source": source})

        return payload

    def __init__(
            self,
            action: str = None,
            affected_assets: List[Dict] = None,
            counter: int = None,
            description: str = None,
            destination: Dict = None,
            destination_affected_asset: Dict = None,
            destination_ip: str = None,
            destination_mac: str = None,
            destination_port: int = None,
            destination_port_str: str = None,
            direction: str = None,
            doc_version: int = None,
            dp_state: str = None,
            event_source: str = None,
            event_source_hostname: str = None,
            event_type: str = None,
            id: str = None,
            incident_id: str = None,
            is_experimental: bool = None,
            network_id: str = None,
            opcode: int = None,
            policy_rule_id: str = None,
            processed_time: str = None,
            received_time: int = None,
            redirect_reason: str = None,
            reversed: bool = None,
            segment_id: int = None,
            source: Dict = None,
            source_affected_asset: Dict = None,
            source_ip: str = None,
            source_mac: str = None,
            source_port: int = None,
            source_vm_id: str = None,
            tag_refs: List = None,
            time: str = None,
            uuid: str = None,
            _cls: str = None,
            **kwargs,
    ):
        self.action = action
        self.affected_assets = affected_assets
        self.counter = counter
        self.description = description
        self.destination = destination
        self.destination_affected_asset = destination_affected_asset
        self.destination_ip = destination_ip
        self.destination_mac = destination_mac
        self.destination_port = destination_port
        self.destination_port_str = destination_port_str
        self.direction = direction
        self.doc_version = doc_version
        self.dp_state = dp_state
        self.event_source = event_source
        self.event_source_hostname = event_source_hostname
        self.event_type = event_type
        self.id = id
        self.incident_id = incident_id
        self.is_experimental = is_experimental
        self.network_id = network_id
        self.opcode = opcode
        self.policy_rule_id = policy_rule_id
        self.processed_time = processed_time
        self.received_time = received_time
        self.redirect_reason = redirect_reason
        self.reversed = reversed
        self.segment_id = segment_id
        self.source = source
        self.source_affected_asset = source_affected_asset
        self.source_ip = source_ip
        self.source_mac = source_mac
        self.source_port = source_port
        self.source_vm_id = source_vm_id
        self.tag_refs = tag_refs
        self.time = time
        self.uuid = uuid
        self._cls = _cls
        if kwargs:
            logging.debug("RedirectionsLog init: unexpected kwargs - %s", kwargs)


class ReputationLog(CentraEntity):
    __path = "/reputation-log"

    def __repr__(self):
        return f"Reputation Log: asset_ip: {self.asset_ip}, requested_ip: {self.requested_ip}"

    @staticmethod
    def list(
            from_time: Union[datetime, timedelta, int, str] = timedelta(days=-1),  # REQUIRED: Incident search range.
            to_time: Union[datetime, timedelta, int, str] = datetime.utcnow(),  # REQUIRED: Incident search range
            asset: Union[str, List[str]] = None,
            origin: Union[str, List[str]] = None,
            request_content: Union[str, List[str]] = None,
            request_type: Union[str, List[str]] = None,
            response: Union[str, List[str]] = None,
            sort: Union[str, List[str]] = None,
    ) -> CentraApiExportable:
        payload = CentraApiExportable(
            path=ReputationLog.__path, method="GET", return_type=ReputationLog,
            export_suffix='/export', export_view_name="reputation-log",
            params={"from_time": from_time, "to_time": to_time}
        )
        if asset:
            payload.params.update({"asset": asset})
        if origin:
            payload.params.update({"origin": origin})
        if request_content:
            payload.params.update({"request_content": request_content})
        if request_type:
            payload.params.update({"request_type": request_type})
        if response:
            payload.params.update({"response": response})
        if sort:
            payload.params.update({"sort": sort})
        return payload

    def __init__(
            self,
            asset: Dict = None,
            asset_ip: str = None,
            doc_version: int = None,
            id: str = None,
            keys_integer_hash: int = None,
            last_seen: int = None,
            occurrences: int = None,
            origin: str = None,
            request_time: int = None,
            request_type: str = None,
            requested_domain: str = None,
            requested_ip: str = None,
            requested_ip_country: Dict = None,
            response: str = None,
            _id: str = None,
            **kwargs
    ):
        self.asset = asset
        self.asset_ip = asset_ip
        self.doc_version = doc_version
        self.id = id
        self.keys_integer_hash = keys_integer_hash
        self.last_seen = last_seen
        self.occurrences = occurrences
        self.origin = origin
        self.request_time = request_time
        self.request_type = request_type
        self.requested_domain = requested_domain
        self.requested_ip = requested_ip
        self.requested_ip_country = requested_ip_country
        self.response = response
        self._id = _id
        if kwargs:
            logging.debug("Reputation init: unexpected kwargs - %s", kwargs)
