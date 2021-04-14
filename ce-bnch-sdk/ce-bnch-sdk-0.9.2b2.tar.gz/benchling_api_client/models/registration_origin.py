import datetime
from typing import Any, Dict, Optional, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="RegistrationOrigin")


@attr.s(auto_attribs=True)
class RegistrationOrigin:
    """  """

    registered_at: datetime.datetime
    origin_entry_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        registered_at = self.registered_at.isoformat()

        origin_entry_id = self.origin_entry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "registeredAt": registered_at,
                "originEntryId": origin_entry_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        registered_at = isoparse(d.pop("registeredAt"))

        origin_entry_id = d.pop("originEntryId")

        registration_origin = cls(
            registered_at=registered_at,
            origin_entry_id=origin_entry_id,
        )

        return registration_origin
