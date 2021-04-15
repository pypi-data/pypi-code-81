from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.found_group import FoundGroup
from ..types import UNSET, Unset

T = TypeVar("T", bound="FoundGroups")


@attr.s(auto_attribs=True)
class FoundGroups:
    """ The list of groups found in a search, including header text (Showing X of Y matching groups) and total of matched groups. """

    header: Union[Unset, str] = UNSET
    total: Union[Unset, int] = UNSET
    groups: Union[Unset, List[FoundGroup]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        header = self.header
        total = self.total
        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if header is not UNSET:
            field_dict["header"] = header
        if total is not UNSET:
            field_dict["total"] = total
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        header = d.pop("header", UNSET)

        total = d.pop("total", UNSET)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = FoundGroup.from_dict(groups_item_data)

            groups.append(groups_item)

        found_groups = cls(
            header=header,
            total=total,
            groups=groups,
        )

        return found_groups
