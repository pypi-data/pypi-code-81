from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.version_usage_in_custom_field import VersionUsageInCustomField
from ..types import UNSET, Unset

T = TypeVar("T", bound="VersionIssueCounts")


@attr.s(auto_attribs=True)
class VersionIssueCounts:
    """ Various counts of issues within a version. """

    self_: Union[Unset, str] = UNSET
    issues_fixed_count: Union[Unset, int] = UNSET
    issues_affected_count: Union[Unset, int] = UNSET
    issue_count_with_custom_fields_showing_version: Union[Unset, int] = UNSET
    custom_field_usage: Union[Unset, List[VersionUsageInCustomField]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        issues_fixed_count = self.issues_fixed_count
        issues_affected_count = self.issues_affected_count
        issue_count_with_custom_fields_showing_version = self.issue_count_with_custom_fields_showing_version
        custom_field_usage: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.custom_field_usage, Unset):
            custom_field_usage = []
            for custom_field_usage_item_data in self.custom_field_usage:
                custom_field_usage_item = custom_field_usage_item_data.to_dict()

                custom_field_usage.append(custom_field_usage_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if issues_fixed_count is not UNSET:
            field_dict["issuesFixedCount"] = issues_fixed_count
        if issues_affected_count is not UNSET:
            field_dict["issuesAffectedCount"] = issues_affected_count
        if issue_count_with_custom_fields_showing_version is not UNSET:
            field_dict["issueCountWithCustomFieldsShowingVersion"] = issue_count_with_custom_fields_showing_version
        if custom_field_usage is not UNSET:
            field_dict["customFieldUsage"] = custom_field_usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        issues_fixed_count = d.pop("issuesFixedCount", UNSET)

        issues_affected_count = d.pop("issuesAffectedCount", UNSET)

        issue_count_with_custom_fields_showing_version = d.pop("issueCountWithCustomFieldsShowingVersion", UNSET)

        custom_field_usage = []
        _custom_field_usage = d.pop("customFieldUsage", UNSET)
        for custom_field_usage_item_data in _custom_field_usage or []:
            custom_field_usage_item = VersionUsageInCustomField.from_dict(custom_field_usage_item_data)

            custom_field_usage.append(custom_field_usage_item)

        version_issue_counts = cls(
            self_=self_,
            issues_fixed_count=issues_fixed_count,
            issues_affected_count=issues_affected_count,
            issue_count_with_custom_fields_showing_version=issue_count_with_custom_fields_showing_version,
            custom_field_usage=custom_field_usage,
        )

        return version_issue_counts
