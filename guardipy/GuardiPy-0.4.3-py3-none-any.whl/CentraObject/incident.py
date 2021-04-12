"""
    Contains interactions with the API relating to Incidents.
"""
import logging
from typing import Iterable, Union, List
from typing_extensions import Literal
from GuardiPy.CentraObject.event import Event
from GuardiPy.CentraObject.vm import VM
from GuardiPy.CentraObject.auxiliary_types import (
    ConcatenatedTag,
    NetworkDestination,
    IncidentGroup,
    IOC,
    BareMinimumAsset,
    Recommendation,
    LabelMinimal
)
from GuardiPy.helpers import CentraEntity, CentraApiExportable, CentraApiPayload
from GuardiPy.CentraObject.Validation import (
    fits_schema,
    SEVERITY,
    INCIDENT_TYPE,
    PREFIXED_FILTER,
    DIRECTION,
    SENSOR_TYPE,
    CLS
)
from datetime import timedelta, datetime


class AffectedAsset(CentraEntity):
    """ Briefly describes an asset that has been affected by an Incident. """

    def __repr__(self):
        return f"AffectedAsset {self.ip} (VM: {self.vm_id})"

    def __init__(
            self,
            country: str = None,
            country_code: str = None,
            ip: str = None,
            is_inner: bool = None,
            labels: List[str] = None,
            vm: dict = None,
            vm_id: str = None,

            # UNDOCUMENTED ADDITIONS #
            domain: str = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"AffectedAsset init: unexpected kwargs?:  {kwargs}")
        self.country = country
        self.country_code = country_code
        self.ip = ip
        self.is_inner = is_inner
        self.labels: List[str] = labels or []
        self.vm = VM(**vm) if vm else None
        self.vm_id = vm_id

        self.domain = domain


class PointedAsset(CentraEntity):  # TODO - Subclassing? AffectedAsset is basically this w/ two extra attributes...
    """ Briefly describes an asset that has been targeted by an Incident.
        Specifically. Asset.source_asset and Asset.destination_asset. """

    def __repr__(self):
        return f"PointedAsset {self.ip} (VM: {self.vm_id})"

    def __init__(
            self,
            ip: str = None,
            is_inner: bool = None,
            labels: List[str] = None,
            vm: dict = None,
            vm_id: str = None,

            # UNDOCUMENTED ADDITIONS #
            domain: str = None,
            country_code: str = None,
            country: str = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"PointedAsset init: unexpected kwargs?:  {kwargs}")
        self.ip = ip
        self.is_inner = is_inner
        self.labels: List[str] = labels or []
        self.vm = VM(**vm) if vm else None
        self.vm_id = vm_id

        self.domain = domain
        self.country_code = country_code
        self.country = country


class Incident(CentraEntity):
    _path = "/incidents"
    _export_suffix = "/export"

    @staticmethod
    def list(
            from_time: Union[datetime, timedelta, int, str] = timedelta(days=-7),  # REQUIRED: Incident search range.
            to_time: Union[datetime, timedelta, int, str] = datetime.utcnow(),  # REQUIRED: Incident search range

            from_closed_time: Union[datetime, timedelta, int, str] = None,  # Incidents closed after this time
            to_closed_time: Union[datetime, timedelta, int, str] = None,  # Incidents closed before this time

            id: Union[str, Iterable[str]] = None,  # UUID(s) to search for/through,
            severity: Union[
                Literal["Low", "Medium", "High"],
                List[Literal["Low", "Medium", "High"]]
            ] = None,  # Incident Severity to search for. Schema Reference: SEVERITY
            incident_group: Union[str, Iterable[str]] = None,  # Incident Group(s) to search for/through
            incident_type: Union[
                Literal['Incident', 'Deception', 'Network Scan', 'Reveal', 'Experimental'],
                List[Literal['Incident', 'Deception', 'Network Scan', 'Reveal', 'Experimental']]
            ] = None,  # Incident Type(s) to search for/through. Schema Reference: INCIDENT_TYPE
            assets: Union[str, Iterable[str]] = None,  # Asset(s) to search for via Source or Dest. Docs ex = IPs.
            source: Union[str, Iterable[str]] = None,  # Asset(s) to search for via Source. Docs ex = FQDN.
            destination: Union[str, Iterable[str]] = None,  # Asset(s) to search for via Dest. Docs ex = FQDN.
            any_side: Union[str, Iterable[str]] = None,  # Search for either Source or Destination tags.
            tags_include: Union[str, Iterable[str]] = None,  # Include items tagged with these only.
            tags_exclude: Union[str, Iterable[str]] = None,  # Exclude items tagged with these.

            sort_by_property: Union[str, Iterable[str]] = None,  # Incident property to sort by
            sort_order: Literal["asc", "desc"] = "asc",  # Default sort order is ascending.

            prefixed_filter: Literal["lateral_movements", "policy_violations", "network_scans", "bad_reputation",
                                     "integrity_violations"] = None  # Schema Reference: PREFIXED_FILTER
    ) -> CentraApiExportable:
        """
            List all incidents.  -GC Docs
            from_time and to_time are required - timezones are in UTC Epoch Milliseconds.
            Default: search incidents within the last 7 days.
        """

        assert from_time  # Check for missing required parameter (per API docs)
        assert to_time  # Check for missing required parameter (per API docs)

        export_view_name = "incidents"
        if fits_schema(prefixed_filter, PREFIXED_FILTER):
            export_view_name += f"_{prefixed_filter}"

        payload = CentraApiExportable(
            path=Incident._path, method="GET", return_type=Incident,
            export_suffix="/export", export_view_name=export_view_name,
            # see https://git.vcjames.io/soc/GuardiPy/issues/8
            params={"from_time": from_time, "to_time": to_time}
        )

        if id:
            payload.params['id'] = id
        if fits_schema(severity, SEVERITY):
            if isinstance(severity, list):
                payload.params['severity'] = ','.join(severity)
            else:
                payload.params['severity'] = severity
        if incident_group:
            # TODO - Add sanity checking. Do these start with "GRP-"? or?
            payload.params['incident_group'] = incident_group
        if fits_schema(incident_type, INCIDENT_TYPE):
            payload.params['incident_type'] = incident_type
        if assets:
            payload.params['assets'] = assets
        if source:
            payload.params['source'] = source
        if destination:
            payload.params['destination'] = destination
        if any_side:
            payload.params['any_side'] = any_side
        if tags_include:
            payload.params['tag'] = tags_include
        if tags_exclude:
            payload.params['tags__not'] = tags_exclude

        if from_closed_time:
            payload.params['from_closed_time'] = from_closed_time
        if to_closed_time:
            payload.params['to_closed_time'] = to_closed_time

        if sort_by_property:  # TODO - Move these to pagination request wrapper?
            payload.params['sort'] = f"{'-' if sort_order == 'desc' else '+'}{sort_by_property}"  # ex -last_seen

        if fits_schema(prefixed_filter, PREFIXED_FILTER):
            payload.params["prefixed_filter"] = prefixed_filter

        return payload

    @staticmethod
    def get_all_info(  # get information on one incident (including events)
            id: str,  # GUID of the event to be searched for
            include_graph_data: bool = False,  # TBD?
    ) -> CentraApiPayload:
        """
            Get information about one incident. Undocumented by the API.
        """

        payload = CentraApiPayload(
            path=f"{Incident._path}/{id}", method="GET",
            return_type=Incident, params={}, response_pagination=False
        )

        return payload

    def __repr__(self):
        return f"{self.incident_type} Incident re: {len(self.affected_assets)} assets."

    def __init__(  # Incident return-type.
            self,
            affected_assets: List[dict] = None,
            closed_time: Union[int, datetime] = None,
            concatenated_tags: List[dict] = None,
            destination_asset: dict = None,
            destination_net: str = None,
            destinations: List[dict] = None,
            direction: str = None,
            doc_version: int = None,
            end_time: Union[int, datetime] = None,
            ended: bool = None,
            enriched: bool = None,
            events: List[dict] = None,  # event.Event
            experimental_id: str = None,
            first_asset: dict = None,  # auxiliary_types.FirstAsset
            flow_ids: List[str] = None,
            has_export: bool = None,
            has_policy_violations: bool = None,
            id: str = None,
            incident_group: List[dict] = None,  # auxiliary_types.IncidentGroup
            incident_type: str = None,
            iocs: List[dict] = None,  # auxiliary_types.IOC
            is_experimental: bool = None,
            labels: List[str] = None,
            last_updated_time: int = None,
            originl_id: str = None,
            policy_revision: int = None,
            processed_events_count: int = None,  # in api docs as "eventS" ...? possibly with capital S as key name!!
            recommendations: List[dict] = None,  # auxiliary_types.Recommendation
            reenrich_count: int = None,
            remote_index: str = None,
            second_asset: dict = None,
            sensor_name: str = None,
            sensor_type: str = None,
            severity: int = None,
            similarity_calculated: bool = None,
            source_asset: dict = None,
            source_vm: dict = None,
            source_vm_id: str = None,
            source_ip: str = None,
            start_time: int = None,  # bigint
            total_events_count: int = None,
            _cls: str = None,
            _id: str = None,  # same as .id?

            # UNDOCUMENTED ADDITIONS #
            original_id: str = None,
            **kwargs
    ):
        if kwargs:
            logging.debug(f"Incident init: unexpected kwargs: {kwargs}")

        self.affected_assets: List[AffectedAsset] = [AffectedAsset(**item) for item in
                                                     (affected_assets or [])]
        self.closed_time = closed_time
        self.concatenated_tags: List[ConcatenatedTag] = [ConcatenatedTag(**item) for item in
                                                         (concatenated_tags or [])]
        self.destination_asset = PointedAsset(**destination_asset) if destination_asset else None
        self.destination_net = destination_net
        self.destinations: List[NetworkDestination] = [NetworkDestination(**item) for item in
                                                       (destinations or [])]
        self.direction = direction if fits_schema(direction, DIRECTION) else None
        self.doc_version = doc_version
        self.end_time = end_time
        self.ended = ended
        self.enriched = enriched
        self.events: List[Event] = [Event(**item) for item in
                                    (events or [])]
        self.experimental_id = experimental_id
        self.first_asset = BareMinimumAsset(**first_asset) if first_asset else None
        self.flow_ids = flow_ids or []
        self.has_export = has_export
        self.has_policy_violations = has_policy_violations
        self.id = id
        self.incident_group: List[IncidentGroup] = [IncidentGroup(**item) for item in
                                                    (incident_group or [])]
        self.incident_type = incident_type
        self.iocs: List[IOC] = [IOC(**item) for item in
                                (iocs or [])]
        self.is_experimental = is_experimental
        self.labels = [LabelMinimal(**item) for item in (labels or [])]
        self.last_updated_time = last_updated_time
        self.originl_id = originl_id
        self.policy_revision = policy_revision
        self.processed_events_count = processed_events_count
        self.recommendations: List[Recommendation] = [Recommendation(**item) for item in
                                                      (recommendations or [])]
        self.reenrich_count = reenrich_count
        self.remote_index = remote_index
        self.second_asset = BareMinimumAsset(**second_asset) if second_asset else None
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type if fits_schema(sensor_type, SENSOR_TYPE) else None
        self.severity = severity
        self.similarity_calculated = similarity_calculated
        self.source_asset = PointedAsset(**source_asset) if source_asset else None
        self.source_vm = VM(**source_vm) if source_vm else None
        self.source_vm_id = source_vm_id
        self.source_ip = source_ip
        self.start_time = start_time
        self.total_events_count = total_events_count
        self._cls = _cls if fits_schema(_cls, CLS) else None
        self._id = _id

        self.original_id = original_id
