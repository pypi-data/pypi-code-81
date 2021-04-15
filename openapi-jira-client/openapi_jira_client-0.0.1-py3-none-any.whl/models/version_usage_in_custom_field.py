from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VersionUsageInCustomField")


@attr.s(auto_attribs=True)
class VersionUsageInCustomField:
    """ List of custom fields using the version. """

    field_name: Union[Unset, str] = UNSET
    custom_field_id: Union[Unset, int] = UNSET
    issue_count_with_version_in_custom_field: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field_name = self.field_name
        custom_field_id = self.custom_field_id
        issue_count_with_version_in_custom_field = self.issue_count_with_version_in_custom_field

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if field_name is not UNSET:
            field_dict["fieldName"] = field_name
        if custom_field_id is not UNSET:
            field_dict["customFieldId"] = custom_field_id
        if issue_count_with_version_in_custom_field is not UNSET:
            field_dict["issueCountWithVersionInCustomField"] = issue_count_with_version_in_custom_field

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_name = d.pop("fieldName", UNSET)

        custom_field_id = d.pop("customFieldId", UNSET)

        issue_count_with_version_in_custom_field = d.pop("issueCountWithVersionInCustomField", UNSET)

        version_usage_in_custom_field = cls(
            field_name=field_name,
            custom_field_id=custom_field_id,
            issue_count_with_version_in_custom_field=issue_count_with_version_in_custom_field,
        )

        return version_usage_in_custom_field
