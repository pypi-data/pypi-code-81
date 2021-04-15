from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="IssueTypeSchemeID")


@attr.s(auto_attribs=True)
class IssueTypeSchemeID:
    """ The ID of an issue type scheme. """

    issue_type_scheme_id: str

    def to_dict(self) -> Dict[str, Any]:
        issue_type_scheme_id = self.issue_type_scheme_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeSchemeId": issue_type_scheme_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_scheme_id = d.pop("issueTypeSchemeId")

        issue_type_scheme_id = cls(
            issue_type_scheme_id=issue_type_scheme_id,
        )

        return issue_type_scheme_id
