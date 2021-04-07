"""
    Contains interactions with the API relating to Assets.
"""
import logging
from typing import Iterable, Union, List
from GuardiPy.helpers import CentraApiPayload, CentraEntity


class Asset(CentraEntity):
    _path = "/assets"

    @staticmethod
    def list(
            search: str = None,  # Name or IP address to search with
            status: Union[str, List[str]] = None,  # Only assets turn off/on
            asset_id: Union[Iterable[str], str] = None,  # Get one or many assets by id
            label_id: Union[Iterable[str], str] = None,  # Get assets by one or many label id
            label_group_id: Union[Iterable[str], str] = None,  # Get assets by one or many label group id
            sort_by_property: str = None,  # Asset property to sort by
            sort_order: str = "asc",  # Default sort order is ascending.
    ) -> CentraApiPayload:
        """ List all of the data center assets the platform is monitoring,
        optionally filtered by a number of criteria.

        The reply includes a list of all Virtual Machines, and for each one whether
        a visibility agent is properly installed and running on it.

        The list includes, by default, machines that were seen in the past and are no longer active."""

        payload = CentraApiPayload(path=Asset._path, method="GET", return_type=Asset)
        if search:
            payload.params['search'] = search
        if status in ["on", "off"]:
            payload.params['status'] = status
        if asset_id:
            # TODO - Add sanity checking. Docs state these are strings beginning with "vm:"
            payload.params['asset'] = asset_id
        if label_id:
            payload.params['labels'] = label_id
        if label_group_id:
            payload.params['label_groups'] = label_group_id

        if sort_by_property:  # TODO - Move these to pagination request wrapper?
            payload.params['sort'] = f"{'-' if sort_order == 'desc' else '+'}{sort_by_property}"  # ex -last_seen
        return payload

    def __init__(
            self,
            full_name: str = None,
            id: str = None,
            last_seen: int = None,
            **kwargs
    ):
        self.full_name = full_name
        self.id = id
        self.last_seen = last_seen
        if kwargs:
            logging.debug("Asset init: unexpected kwargs - %s", kwargs)
