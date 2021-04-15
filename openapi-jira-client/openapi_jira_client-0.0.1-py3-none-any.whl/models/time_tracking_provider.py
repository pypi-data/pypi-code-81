from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeTrackingProvider")


@attr.s(auto_attribs=True)
class TimeTrackingProvider:
    """ Details about the time tracking provider. """

    key: str
    name: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        name = self.name
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "key": key,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        time_tracking_provider = cls(
            key=key,
            name=name,
            url=url,
        )

        return time_tracking_provider
