from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_component_assignee_type import ComponentsschemasComponentAssigneeType
from ..models.componentsschemas_component_real_assignee_type import ComponentsschemasComponentRealAssigneeType
from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="Component")


@attr.s(auto_attribs=True)
class Component:
    """ Details about a project component. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    lead: Union[Unset, User] = UNSET
    lead_user_name: Union[Unset, str] = UNSET
    lead_account_id: Union[Unset, str] = UNSET
    assignee_type: Union[Unset, ComponentsschemasComponentAssigneeType] = UNSET
    assignee: Union[Unset, User] = UNSET
    real_assignee_type: Union[Unset, ComponentsschemasComponentRealAssigneeType] = UNSET
    real_assignee: Union[Unset, User] = UNSET
    is_assignee_type_valid: Union[Unset, bool] = UNSET
    project: Union[Unset, str] = UNSET
    project_id: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        name = self.name
        description = self.description
        lead: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lead, Unset):
            lead = self.lead.to_dict()

        lead_user_name = self.lead_user_name
        lead_account_id = self.lead_account_id
        assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.assignee_type, Unset):
            assignee_type = self.assignee_type.value

        assignee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.assignee, Unset):
            assignee = self.assignee.to_dict()

        real_assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.real_assignee_type, Unset):
            real_assignee_type = self.real_assignee_type.value

        real_assignee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.real_assignee, Unset):
            real_assignee = self.real_assignee.to_dict()

        is_assignee_type_valid = self.is_assignee_type_valid
        project = self.project
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if lead is not UNSET:
            field_dict["lead"] = lead
        if lead_user_name is not UNSET:
            field_dict["leadUserName"] = lead_user_name
        if lead_account_id is not UNSET:
            field_dict["leadAccountId"] = lead_account_id
        if assignee_type is not UNSET:
            field_dict["assigneeType"] = assignee_type
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if real_assignee_type is not UNSET:
            field_dict["realAssigneeType"] = real_assignee_type
        if real_assignee is not UNSET:
            field_dict["realAssignee"] = real_assignee
        if is_assignee_type_valid is not UNSET:
            field_dict["isAssigneeTypeValid"] = is_assignee_type_valid
        if project is not UNSET:
            field_dict["project"] = project
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        lead: Union[Unset, User] = UNSET
        _lead = d.pop("lead", UNSET)
        if not isinstance(_lead, Unset):
            lead = User.from_dict(_lead)

        lead_user_name = d.pop("leadUserName", UNSET)

        lead_account_id = d.pop("leadAccountId", UNSET)

        assignee_type: Union[Unset, ComponentsschemasComponentAssigneeType] = UNSET
        _assignee_type = d.pop("assigneeType", UNSET)
        if not isinstance(_assignee_type, Unset):
            assignee_type = ComponentsschemasComponentAssigneeType(_assignee_type)

        assignee: Union[Unset, User] = UNSET
        _assignee = d.pop("assignee", UNSET)
        if not isinstance(_assignee, Unset):
            assignee = User.from_dict(_assignee)

        real_assignee_type: Union[Unset, ComponentsschemasComponentRealAssigneeType] = UNSET
        _real_assignee_type = d.pop("realAssigneeType", UNSET)
        if not isinstance(_real_assignee_type, Unset):
            real_assignee_type = ComponentsschemasComponentRealAssigneeType(_real_assignee_type)

        real_assignee: Union[Unset, User] = UNSET
        _real_assignee = d.pop("realAssignee", UNSET)
        if not isinstance(_real_assignee, Unset):
            real_assignee = User.from_dict(_real_assignee)

        is_assignee_type_valid = d.pop("isAssigneeTypeValid", UNSET)

        project = d.pop("project", UNSET)

        project_id = d.pop("projectId", UNSET)

        component = cls(
            self_=self_,
            id_=id_,
            name=name,
            description=description,
            lead=lead,
            lead_user_name=lead_user_name,
            lead_account_id=lead_account_id,
            assignee_type=assignee_type,
            assignee=assignee,
            real_assignee_type=real_assignee_type,
            real_assignee=real_assignee,
            is_assignee_type_valid=is_assignee_type_valid,
            project=project,
            project_id=project_id,
        )

        return component
