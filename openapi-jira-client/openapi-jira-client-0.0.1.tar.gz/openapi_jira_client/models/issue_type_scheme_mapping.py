from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="IssueTypeSchemeMapping")


@attr.s(auto_attribs=True)
class IssueTypeSchemeMapping:
    """ Issue type scheme item. """

    issue_type_scheme_id: str
    issue_type_id: str

    def to_dict(self) -> Dict[str, Any]:
        issue_type_scheme_id = self.issue_type_scheme_id
        issue_type_id = self.issue_type_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeSchemeId": issue_type_scheme_id,
                "issueTypeId": issue_type_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_scheme_id = d.pop("issueTypeSchemeId")

        issue_type_id = d.pop("issueTypeId")

        issue_type_scheme_mapping = cls(
            issue_type_scheme_id=issue_type_scheme_id,
            issue_type_id=issue_type_id,
        )

        return issue_type_scheme_mapping
