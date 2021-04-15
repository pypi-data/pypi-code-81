from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypesWorkflowMapping")


@attr.s(auto_attribs=True)
class IssueTypesWorkflowMapping:
    """ Details about the mapping between issue types and a workflow. """

    workflow: Union[Unset, str] = UNSET
    issue_types: Union[Unset, List[str]] = UNSET
    default_mapping: Union[Unset, bool] = UNSET
    update_draft_if_needed: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        workflow = self.workflow
        issue_types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.issue_types, Unset):
            issue_types = self.issue_types

        default_mapping = self.default_mapping
        update_draft_if_needed = self.update_draft_if_needed

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if workflow is not UNSET:
            field_dict["workflow"] = workflow
        if issue_types is not UNSET:
            field_dict["issueTypes"] = issue_types
        if default_mapping is not UNSET:
            field_dict["defaultMapping"] = default_mapping
        if update_draft_if_needed is not UNSET:
            field_dict["updateDraftIfNeeded"] = update_draft_if_needed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow = d.pop("workflow", UNSET)

        issue_types = cast(List[str], d.pop("issueTypes", UNSET))

        default_mapping = d.pop("defaultMapping", UNSET)

        update_draft_if_needed = d.pop("updateDraftIfNeeded", UNSET)

        issue_types_workflow_mapping = cls(
            workflow=workflow,
            issue_types=issue_types,
            default_mapping=default_mapping,
            update_draft_if_needed=update_draft_if_needed,
        )

        return issue_types_workflow_mapping
