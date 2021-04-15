from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.icon import Icon
from ..models.status import Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteObject")


@attr.s(auto_attribs=True)
class RemoteObject:
    """ The linked item. """

    url: str
    title: str
    summary: Union[Unset, str] = UNSET
    icon: Union[Unset, Icon] = UNSET
    status: Union[Unset, Status] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        title = self.title
        summary = self.summary
        icon: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.icon, Unset):
            icon = self.icon.to_dict()

        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "title": title,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if icon is not UNSET:
            field_dict["icon"] = icon
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        title = d.pop("title")

        summary = d.pop("summary", UNSET)

        icon: Union[Unset, Icon] = UNSET
        _icon = d.pop("icon", UNSET)
        if not isinstance(_icon, Unset):
            icon = Icon.from_dict(_icon)

        status: Union[Unset, Status] = UNSET
        _status = d.pop("status", UNSET)
        if not isinstance(_status, Unset):
            status = Status.from_dict(_status)

        remote_object = cls(
            url=url,
            title=title,
            summary=summary,
            icon=icon,
            status=status,
        )

        remote_object.additional_properties = d
        return remote_object

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
