from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkflowStatusProperties")


@attr.s(auto_attribs=True)
class WorkflowStatusProperties:
    """ Properties of a workflow status. """

    issue_editable: bool

    def to_dict(self) -> Dict[str, Any]:
        issue_editable = self.issue_editable

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueEditable": issue_editable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_editable = d.pop("issueEditable")

        workflow_status_properties = cls(
            issue_editable=issue_editable,
        )

        return workflow_status_properties
