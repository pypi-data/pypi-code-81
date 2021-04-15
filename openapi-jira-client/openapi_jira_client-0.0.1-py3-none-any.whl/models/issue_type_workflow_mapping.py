from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeWorkflowMapping")


@attr.s(auto_attribs=True)
class IssueTypeWorkflowMapping:
    """ Details about the mapping between an issue type and a workflow. """

    issue_type: Union[Unset, str] = UNSET
    workflow: Union[Unset, str] = UNSET
    update_draft_if_needed: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_type = self.issue_type
        workflow = self.workflow
        update_draft_if_needed = self.update_draft_if_needed

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_type is not UNSET:
            field_dict["issueType"] = issue_type
        if workflow is not UNSET:
            field_dict["workflow"] = workflow
        if update_draft_if_needed is not UNSET:
            field_dict["updateDraftIfNeeded"] = update_draft_if_needed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type = d.pop("issueType", UNSET)

        workflow = d.pop("workflow", UNSET)

        update_draft_if_needed = d.pop("updateDraftIfNeeded", UNSET)

        issue_type_workflow_mapping = cls(
            issue_type=issue_type,
            workflow=workflow,
            update_draft_if_needed=update_draft_if_needed,
        )

        return issue_type_workflow_mapping
