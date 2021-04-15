from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_workflow_scheme_issue_type_mappings import (
    ComponentsschemasWorkflowSchemeIssueTypeMappings,
)
from ..models.componentsschemas_workflow_scheme_issue_types import ComponentsschemasWorkflowSchemeIssueTypes
from ..models.componentsschemas_workflow_scheme_original_issue_type_mappings import (
    ComponentsschemasWorkflowSchemeOriginalIssueTypeMappings,
)
from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowScheme")


@attr.s(auto_attribs=True)
class WorkflowScheme:
    """ Details about a workflow scheme. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    default_workflow: Union[Unset, str] = UNSET
    issue_type_mappings: Union[Unset, ComponentsschemasWorkflowSchemeIssueTypeMappings] = UNSET
    original_default_workflow: Union[Unset, str] = UNSET
    original_issue_type_mappings: Union[Unset, ComponentsschemasWorkflowSchemeOriginalIssueTypeMappings] = UNSET
    draft: Union[Unset, bool] = UNSET
    last_modified_user: Union[Unset, User] = UNSET
    last_modified: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    update_draft_if_needed: Union[Unset, bool] = UNSET
    issue_types: Union[Unset, ComponentsschemasWorkflowSchemeIssueTypes] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        default_workflow = self.default_workflow
        issue_type_mappings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issue_type_mappings, Unset):
            issue_type_mappings = self.issue_type_mappings.to_dict()

        original_default_workflow = self.original_default_workflow
        original_issue_type_mappings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.original_issue_type_mappings, Unset):
            original_issue_type_mappings = self.original_issue_type_mappings.to_dict()

        draft = self.draft
        last_modified_user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_modified_user, Unset):
            last_modified_user = self.last_modified_user.to_dict()

        last_modified = self.last_modified
        self_ = self.self_
        update_draft_if_needed = self.update_draft_if_needed
        issue_types: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issue_types, Unset):
            issue_types = self.issue_types.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if default_workflow is not UNSET:
            field_dict["defaultWorkflow"] = default_workflow
        if issue_type_mappings is not UNSET:
            field_dict["issueTypeMappings"] = issue_type_mappings
        if original_default_workflow is not UNSET:
            field_dict["originalDefaultWorkflow"] = original_default_workflow
        if original_issue_type_mappings is not UNSET:
            field_dict["originalIssueTypeMappings"] = original_issue_type_mappings
        if draft is not UNSET:
            field_dict["draft"] = draft
        if last_modified_user is not UNSET:
            field_dict["lastModifiedUser"] = last_modified_user
        if last_modified is not UNSET:
            field_dict["lastModified"] = last_modified
        if self_ is not UNSET:
            field_dict["self"] = self_
        if update_draft_if_needed is not UNSET:
            field_dict["updateDraftIfNeeded"] = update_draft_if_needed
        if issue_types is not UNSET:
            field_dict["issueTypes"] = issue_types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        default_workflow = d.pop("defaultWorkflow", UNSET)

        issue_type_mappings: Union[Unset, ComponentsschemasWorkflowSchemeIssueTypeMappings] = UNSET
        _issue_type_mappings = d.pop("issueTypeMappings", UNSET)
        if not isinstance(_issue_type_mappings, Unset):
            issue_type_mappings = ComponentsschemasWorkflowSchemeIssueTypeMappings.from_dict(_issue_type_mappings)

        original_default_workflow = d.pop("originalDefaultWorkflow", UNSET)

        original_issue_type_mappings: Union[Unset, ComponentsschemasWorkflowSchemeOriginalIssueTypeMappings] = UNSET
        _original_issue_type_mappings = d.pop("originalIssueTypeMappings", UNSET)
        if not isinstance(_original_issue_type_mappings, Unset):
            original_issue_type_mappings = ComponentsschemasWorkflowSchemeOriginalIssueTypeMappings.from_dict(
                _original_issue_type_mappings
            )

        draft = d.pop("draft", UNSET)

        last_modified_user: Union[Unset, User] = UNSET
        _last_modified_user = d.pop("lastModifiedUser", UNSET)
        if not isinstance(_last_modified_user, Unset):
            last_modified_user = User.from_dict(_last_modified_user)

        last_modified = d.pop("lastModified", UNSET)

        self_ = d.pop("self", UNSET)

        update_draft_if_needed = d.pop("updateDraftIfNeeded", UNSET)

        issue_types: Union[Unset, ComponentsschemasWorkflowSchemeIssueTypes] = UNSET
        _issue_types = d.pop("issueTypes", UNSET)
        if not isinstance(_issue_types, Unset):
            issue_types = ComponentsschemasWorkflowSchemeIssueTypes.from_dict(_issue_types)

        workflow_scheme = cls(
            id_=id_,
            name=name,
            description=description,
            default_workflow=default_workflow,
            issue_type_mappings=issue_type_mappings,
            original_default_workflow=original_default_workflow,
            original_issue_type_mappings=original_issue_type_mappings,
            draft=draft,
            last_modified_user=last_modified_user,
            last_modified=last_modified,
            self_=self_,
            update_draft_if_needed=update_draft_if_needed,
            issue_types=issue_types,
        )

        return workflow_scheme
