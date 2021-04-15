from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueFilterForBulkPropertyDelete")


@attr.s(auto_attribs=True)
class IssueFilterForBulkPropertyDelete:
    """ Bulk operation filter details. """

    entity_ids: Union[Unset, List[int]] = UNSET
    current_value: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        entity_ids: Union[Unset, List[int]] = UNSET
        if not isinstance(self.entity_ids, Unset):
            entity_ids = self.entity_ids

        current_value = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if entity_ids is not UNSET:
            field_dict["entityIds"] = entity_ids
        if current_value is not UNSET:
            field_dict["currentValue"] = current_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_ids = cast(List[int], d.pop("entityIds", UNSET))

        current_value = None

        issue_filter_for_bulk_property_delete = cls(
            entity_ids=entity_ids,
            current_value=current_value,
        )

        return issue_filter_for_bulk_property_delete
