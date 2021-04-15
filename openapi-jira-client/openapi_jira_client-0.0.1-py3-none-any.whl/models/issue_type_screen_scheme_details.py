from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.issue_type_screen_scheme_mapping import IssueTypeScreenSchemeMapping
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeScreenSchemeDetails")


@attr.s(auto_attribs=True)
class IssueTypeScreenSchemeDetails:
    """ The details of an issue type screen scheme. """

    name: str
    issue_type_mappings: List[IssueTypeScreenSchemeMapping]
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        issue_type_mappings = []
        for issue_type_mappings_item_data in self.issue_type_mappings:
            issue_type_mappings_item = issue_type_mappings_item_data.to_dict()

            issue_type_mappings.append(issue_type_mappings_item)

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "issueTypeMappings": issue_type_mappings,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        issue_type_mappings = []
        _issue_type_mappings = d.pop("issueTypeMappings")
        for issue_type_mappings_item_data in _issue_type_mappings:
            issue_type_mappings_item = IssueTypeScreenSchemeMapping.from_dict(issue_type_mappings_item_data)

            issue_type_mappings.append(issue_type_mappings_item)

        description = d.pop("description", UNSET)

        issue_type_screen_scheme_details = cls(
            name=name,
            issue_type_mappings=issue_type_mappings,
            description=description,
        )

        return issue_type_screen_scheme_details
