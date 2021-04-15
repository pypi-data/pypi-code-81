from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupDetails")


@attr.s(auto_attribs=True)
class GroupDetails:
    """ Details about a group. """

    name: Union[Unset, str] = UNSET
    group_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        group_id = self.group_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if group_id is not UNSET:
            field_dict["groupId"] = group_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        group_id = d.pop("groupId", UNSET)

        group_details = cls(
            name=name,
            group_id=group_id,
        )

        return group_details
