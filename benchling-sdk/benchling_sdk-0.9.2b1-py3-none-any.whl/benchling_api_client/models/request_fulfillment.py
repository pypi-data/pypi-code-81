import datetime
from typing import Any, Dict, Optional, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.sample_group import SampleGroup
from ..models.sample_group_status import SampleGroupStatus

T = TypeVar("T", bound="RequestFulfillment")


@attr.s(auto_attribs=True)
class RequestFulfillment:
    """A request fulfillment represents work that is done which changes the status of a request or a sample group within that request.
    Fulfillments are created when state changes between IN_PROGRESS, COMPLETED, or FAILED statuses. Fulfillments do not capture a PENDING state because all requests or request sample groups are considered PENDING until the first corresponding fulfillment is created.
    """

    created_at: datetime.datetime
    entry_id: str
    id: str
    request_id: str
    status: SampleGroupStatus
    sample_group: Optional[SampleGroup]

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        entry_id = self.entry_id
        id = self.id
        request_id = self.request_id
        status = self.status.value

        sample_group = self.sample_group.to_dict() if self.sample_group else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdAt": created_at,
                "entryId": entry_id,
                "id": id,
                "requestId": request_id,
                "status": status,
                "sampleGroup": sample_group,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("createdAt"))

        entry_id = d.pop("entryId")

        id = d.pop("id")

        request_id = d.pop("requestId")

        status = SampleGroupStatus(d.pop("status"))

        sample_group = None
        _sample_group = d.pop("sampleGroup")
        if _sample_group is not None:
            sample_group = SampleGroup.from_dict(_sample_group)

        request_fulfillment = cls(
            created_at=created_at,
            entry_id=entry_id,
            id=id,
            request_id=request_id,
            status=status,
            sample_group=sample_group,
        )

        return request_fulfillment
