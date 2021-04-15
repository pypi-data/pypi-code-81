from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.icon import Icon
from ..types import UNSET, Unset

T = TypeVar("T", bound="Status")


@attr.s(auto_attribs=True)
class Status:
    """ The status of the item. """

    resolved: Union[Unset, bool] = UNSET
    icon: Union[Unset, Icon] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resolved = self.resolved
        icon: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.icon, Unset):
            icon = self.icon.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resolved is not UNSET:
            field_dict["resolved"] = resolved
        if icon is not UNSET:
            field_dict["icon"] = icon

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resolved = d.pop("resolved", UNSET)

        icon: Union[Unset, Icon] = UNSET
        _icon = d.pop("icon", UNSET)
        if not isinstance(_icon, Unset):
            icon = Icon.from_dict(_icon)

        status = cls(
            resolved=resolved,
            icon=icon,
        )

        status.additional_properties = d
        return status

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
