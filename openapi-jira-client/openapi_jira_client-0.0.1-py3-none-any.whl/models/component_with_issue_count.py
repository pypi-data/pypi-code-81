from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_component_with_issue_count_assignee_type import (
    ComponentsschemasComponentWithIssueCountAssigneeType,
)
from ..models.componentsschemas_component_with_issue_count_real_assignee_type import (
    ComponentsschemasComponentWithIssueCountRealAssigneeType,
)
from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentWithIssueCount")


@attr.s(auto_attribs=True)
class ComponentWithIssueCount:
    """ Details about a component with a count of the issues it contains. """

    issue_count: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    lead: Union[Unset, User] = UNSET
    assignee_type: Union[Unset, ComponentsschemasComponentWithIssueCountAssigneeType] = UNSET
    project_id: Union[Unset, int] = UNSET
    assignee: Union[Unset, User] = UNSET
    real_assignee: Union[Unset, User] = UNSET
    is_assignee_type_valid: Union[Unset, bool] = UNSET
    real_assignee_type: Union[Unset, ComponentsschemasComponentWithIssueCountRealAssigneeType] = UNSET
    name: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        issue_count = self.issue_count
        description = self.description
        self_ = self.self_
        project = self.project
        lead: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lead, Unset):
            lead = self.lead.to_dict()

        assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.assignee_type, Unset):
            assignee_type = self.assignee_type.value

        project_id = self.project_id
        assignee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.assignee, Unset):
            assignee = self.assignee.to_dict()

        real_assignee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.real_assignee, Unset):
            real_assignee = self.real_assignee.to_dict()

        is_assignee_type_valid = self.is_assignee_type_valid
        real_assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.real_assignee_type, Unset):
            real_assignee_type = self.real_assignee_type.value

        name = self.name
        id_ = self.id_

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if issue_count is not UNSET:
            field_dict["issueCount"] = issue_count
        if description is not UNSET:
            field_dict["description"] = description
        if self_ is not UNSET:
            field_dict["self"] = self_
        if project is not UNSET:
            field_dict["project"] = project
        if lead is not UNSET:
            field_dict["lead"] = lead
        if assignee_type is not UNSET:
            field_dict["assigneeType"] = assignee_type
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if real_assignee is not UNSET:
            field_dict["realAssignee"] = real_assignee
        if is_assignee_type_valid is not UNSET:
            field_dict["isAssigneeTypeValid"] = is_assignee_type_valid
        if real_assignee_type is not UNSET:
            field_dict["realAssigneeType"] = real_assignee_type
        if name is not UNSET:
            field_dict["name"] = name
        if id_ is not UNSET:
            field_dict["id"] = id_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_count = d.pop("issueCount", UNSET)

        description = d.pop("description", UNSET)

        self_ = d.pop("self", UNSET)

        project = d.pop("project", UNSET)

        lead: Union[Unset, User] = UNSET
        _lead = d.pop("lead", UNSET)
        if not isinstance(_lead, Unset):
            lead = User.from_dict(_lead)

        assignee_type: Union[Unset, ComponentsschemasComponentWithIssueCountAssigneeType] = UNSET
        _assignee_type = d.pop("assigneeType", UNSET)
        if not isinstance(_assignee_type, Unset):
            assignee_type = ComponentsschemasComponentWithIssueCountAssigneeType(_assignee_type)

        project_id = d.pop("projectId", UNSET)

        assignee: Union[Unset, User] = UNSET
        _assignee = d.pop("assignee", UNSET)
        if not isinstance(_assignee, Unset):
            assignee = User.from_dict(_assignee)

        real_assignee: Union[Unset, User] = UNSET
        _real_assignee = d.pop("realAssignee", UNSET)
        if not isinstance(_real_assignee, Unset):
            real_assignee = User.from_dict(_real_assignee)

        is_assignee_type_valid = d.pop("isAssigneeTypeValid", UNSET)

        real_assignee_type: Union[Unset, ComponentsschemasComponentWithIssueCountRealAssigneeType] = UNSET
        _real_assignee_type = d.pop("realAssigneeType", UNSET)
        if not isinstance(_real_assignee_type, Unset):
            real_assignee_type = ComponentsschemasComponentWithIssueCountRealAssigneeType(_real_assignee_type)

        name = d.pop("name", UNSET)

        id_ = d.pop("id", UNSET)

        component_with_issue_count = cls(
            issue_count=issue_count,
            description=description,
            self_=self_,
            project=project,
            lead=lead,
            assignee_type=assignee_type,
            project_id=project_id,
            assignee=assignee,
            real_assignee=real_assignee,
            is_assignee_type_valid=is_assignee_type_valid,
            real_assignee_type=real_assignee_type,
            name=name,
            id_=id_,
        )

        return component_with_issue_count
