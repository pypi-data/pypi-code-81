from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.issue_type_screen_scheme_mapping import IssueTypeScreenSchemeMapping

T = TypeVar("T", bound="IssueTypeScreenSchemeMappingDetails")


@attr.s(auto_attribs=True)
class IssueTypeScreenSchemeMappingDetails:
    """ A list of issue type screen scheme mappings. """

    issue_type_mappings: List[IssueTypeScreenSchemeMapping]

    def to_dict(self) -> Dict[str, Any]:
        issue_type_mappings = []
        for issue_type_mappings_item_data in self.issue_type_mappings:
            issue_type_mappings_item = issue_type_mappings_item_data.to_dict()

            issue_type_mappings.append(issue_type_mappings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeMappings": issue_type_mappings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_mappings = []
        _issue_type_mappings = d.pop("issueTypeMappings")
        for issue_type_mappings_item_data in _issue_type_mappings:
            issue_type_mappings_item = IssueTypeScreenSchemeMapping.from_dict(issue_type_mappings_item_data)

            issue_type_mappings.append(issue_type_mappings_item)

        issue_type_screen_scheme_mapping_details = cls(
            issue_type_mappings=issue_type_mappings,
        )

        return issue_type_screen_scheme_mapping_details
