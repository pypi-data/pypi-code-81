from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ContextForProjectAndIssueType")


@attr.s(auto_attribs=True)
class ContextForProjectAndIssueType:
    """ The project and issue type mapping with a matching custom field context. """

    project_id: str
    issue_type_id: str
    context_id: str

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        issue_type_id = self.issue_type_id
        context_id = self.context_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectId": project_id,
                "issueTypeId": issue_type_id,
                "contextId": context_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId")

        issue_type_id = d.pop("issueTypeId")

        context_id = d.pop("contextId")

        context_for_project_and_issue_type = cls(
            project_id=project_id,
            issue_type_id=issue_type_id,
            context_id=context_id,
        )

        return context_for_project_and_issue_type
