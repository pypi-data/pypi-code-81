from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.issue_link_type import IssueLinkType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueLinkTypes")


@attr.s(auto_attribs=True)
class IssueLinkTypes:
    """ A list of issue link type beans. """

    issue_link_types: Union[Unset, List[IssueLinkType]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_link_types: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issue_link_types, Unset):
            issue_link_types = []
            for issue_link_types_item_data in self.issue_link_types:
                issue_link_types_item = issue_link_types_item_data.to_dict()

                issue_link_types.append(issue_link_types_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_link_types is not UNSET:
            field_dict["issueLinkTypes"] = issue_link_types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_link_types = []
        _issue_link_types = d.pop("issueLinkTypes", UNSET)
        for issue_link_types_item_data in _issue_link_types or []:
            issue_link_types_item = IssueLinkType.from_dict(issue_link_types_item_data)

            issue_link_types.append(issue_link_types_item)

        issue_link_types = cls(
            issue_link_types=issue_link_types,
        )

        return issue_link_types
