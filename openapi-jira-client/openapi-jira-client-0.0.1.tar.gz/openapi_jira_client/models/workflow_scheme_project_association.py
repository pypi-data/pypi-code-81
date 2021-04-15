from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowSchemeProjectAssociation")


@attr.s(auto_attribs=True)
class WorkflowSchemeProjectAssociation:
    """ An associated workflow scheme and project. """

    workflow_scheme_id: str
    project_id: str

    def to_dict(self) -> Dict[str, Any]:
        workflow_scheme_id = self.workflow_scheme_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflowSchemeId": workflow_scheme_id,
                "projectId": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_scheme_id = d.pop("workflowSchemeId")

        project_id = d.pop("projectId")

        workflow_scheme_project_association = cls(
            workflow_scheme_id=workflow_scheme_id,
            project_id=project_id,
        )

        return workflow_scheme_project_association
