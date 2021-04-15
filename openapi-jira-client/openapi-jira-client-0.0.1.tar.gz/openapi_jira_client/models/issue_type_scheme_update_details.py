from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeSchemeUpdateDetails")


@attr.s(auto_attribs=True)
class IssueTypeSchemeUpdateDetails:
    """ Details of the name, description, and default issue type for an issue type scheme. """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    default_issue_type_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        default_issue_type_id = self.default_issue_type_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if default_issue_type_id is not UNSET:
            field_dict["defaultIssueTypeId"] = default_issue_type_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        default_issue_type_id = d.pop("defaultIssueTypeId", UNSET)

        issue_type_scheme_update_details = cls(
            name=name,
            description=description,
            default_issue_type_id=default_issue_type_id,
        )

        return issue_type_scheme_update_details
