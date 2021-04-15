from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeSchemeDetails")


@attr.s(auto_attribs=True)
class IssueTypeSchemeDetails:
    """ Details of an issue type scheme and its associated issue types. """

    name: str
    issue_type_ids: List[str]
    description: Union[Unset, str] = UNSET
    default_issue_type_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        issue_type_ids = self.issue_type_ids

        description = self.description
        default_issue_type_id = self.default_issue_type_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "issueTypeIds": issue_type_ids,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if default_issue_type_id is not UNSET:
            field_dict["defaultIssueTypeId"] = default_issue_type_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        issue_type_ids = cast(List[str], d.pop("issueTypeIds"))

        description = d.pop("description", UNSET)

        default_issue_type_id = d.pop("defaultIssueTypeId", UNSET)

        issue_type_scheme_details = cls(
            name=name,
            issue_type_ids=issue_type_ids,
            description=description,
            default_issue_type_id=default_issue_type_id,
        )

        return issue_type_scheme_details
