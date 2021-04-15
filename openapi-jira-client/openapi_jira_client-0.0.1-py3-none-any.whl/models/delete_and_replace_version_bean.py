from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.custom_field_replacement import CustomFieldReplacement
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteAndReplaceVersionBean")


@attr.s(auto_attribs=True)
class DeleteAndReplaceVersionBean:
    """  """

    move_fix_issues_to: Union[Unset, int] = UNSET
    move_affected_issues_to: Union[Unset, int] = UNSET
    custom_field_replacement_list: Union[Unset, List[CustomFieldReplacement]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        move_fix_issues_to = self.move_fix_issues_to
        move_affected_issues_to = self.move_affected_issues_to
        custom_field_replacement_list: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.custom_field_replacement_list, Unset):
            custom_field_replacement_list = []
            for custom_field_replacement_list_item_data in self.custom_field_replacement_list:
                custom_field_replacement_list_item = custom_field_replacement_list_item_data.to_dict()

                custom_field_replacement_list.append(custom_field_replacement_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if move_fix_issues_to is not UNSET:
            field_dict["moveFixIssuesTo"] = move_fix_issues_to
        if move_affected_issues_to is not UNSET:
            field_dict["moveAffectedIssuesTo"] = move_affected_issues_to
        if custom_field_replacement_list is not UNSET:
            field_dict["customFieldReplacementList"] = custom_field_replacement_list

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        move_fix_issues_to = d.pop("moveFixIssuesTo", UNSET)

        move_affected_issues_to = d.pop("moveAffectedIssuesTo", UNSET)

        custom_field_replacement_list = []
        _custom_field_replacement_list = d.pop("customFieldReplacementList", UNSET)
        for custom_field_replacement_list_item_data in _custom_field_replacement_list or []:
            custom_field_replacement_list_item = CustomFieldReplacement.from_dict(
                custom_field_replacement_list_item_data
            )

            custom_field_replacement_list.append(custom_field_replacement_list_item)

        delete_and_replace_version_bean = cls(
            move_fix_issues_to=move_fix_issues_to,
            move_affected_issues_to=move_affected_issues_to,
            custom_field_replacement_list=custom_field_replacement_list,
        )

        return delete_and_replace_version_bean
