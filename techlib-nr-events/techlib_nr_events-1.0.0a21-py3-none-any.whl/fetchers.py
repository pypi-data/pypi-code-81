from __future__ import absolute_import, print_function

from invenio_pidstore.fetchers import FetchedPID
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities

from .providers import NREventsIdProvider


def nr_events_id_fetcher(record_uuid, data):
    """Fetch a record's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    id_field = "control_number"
    return FetchedPID(  # FetchedPID je obyčejný namedtuple
        provider=NREventsIdProvider,
        pid_type=NREventsIdProvider.pid_type,
        pid_value=CommunityPIDValue(
            str(data[id_field]),
            current_oarepo_communities.get_primary_community_field(data))
    )
