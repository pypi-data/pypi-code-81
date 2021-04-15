from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_order_of_issue_types_position import ComponentsschemasOrderOfIssueTypesPosition
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderOfIssueTypes")


@attr.s(auto_attribs=True)
class OrderOfIssueTypes:
    """ An ordered list of issue type IDs and information about where to move them. """

    issue_type_ids: List[str]
    after: Union[Unset, str] = UNSET
    position: Union[Unset, ComponentsschemasOrderOfIssueTypesPosition] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_type_ids = self.issue_type_ids

        after = self.after
        position: Union[Unset, str] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeIds": issue_type_ids,
            }
        )
        if after is not UNSET:
            field_dict["after"] = after
        if position is not UNSET:
            field_dict["position"] = position

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_ids = cast(List[str], d.pop("issueTypeIds"))

        after = d.pop("after", UNSET)

        position: Union[Unset, ComponentsschemasOrderOfIssueTypesPosition] = UNSET
        _position = d.pop("position", UNSET)
        if not isinstance(_position, Unset):
            position = ComponentsschemasOrderOfIssueTypesPosition(_position)

        order_of_issue_types = cls(
            issue_type_ids=issue_type_ids,
            after=after,
            position=position,
        )

        return order_of_issue_types
