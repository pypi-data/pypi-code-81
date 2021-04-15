from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ProjectIssueTypeMapping")


@attr.s(auto_attribs=True)
class ProjectIssueTypeMapping:
    """ The project and issue type mapping. """

    project_id: str
    issue_type_id: str

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        issue_type_id = self.issue_type_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectId": project_id,
                "issueTypeId": issue_type_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId")

        issue_type_id = d.pop("issueTypeId")

        project_issue_type_mapping = cls(
            project_id=project_id,
            issue_type_id=issue_type_id,
        )

        return project_issue_type_mapping
