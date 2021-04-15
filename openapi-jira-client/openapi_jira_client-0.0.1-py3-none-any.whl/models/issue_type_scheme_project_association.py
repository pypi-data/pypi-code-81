from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="IssueTypeSchemeProjectAssociation")


@attr.s(auto_attribs=True)
class IssueTypeSchemeProjectAssociation:
    """ Details of the association between an issue type scheme and project. """

    issue_type_scheme_id: str
    project_id: str

    def to_dict(self) -> Dict[str, Any]:
        issue_type_scheme_id = self.issue_type_scheme_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeSchemeId": issue_type_scheme_id,
                "projectId": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_scheme_id = d.pop("issueTypeSchemeId")

        project_id = d.pop("projectId")

        issue_type_scheme_project_association = cls(
            issue_type_scheme_id=issue_type_scheme_id,
            project_id=project_id,
        )

        return issue_type_scheme_project_association
