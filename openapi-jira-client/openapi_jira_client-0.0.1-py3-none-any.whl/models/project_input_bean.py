from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_project_input_bean_assignee_type import ComponentsschemasProjectInputBeanAssigneeType
from ..models.componentsschemas_project_input_bean_project_template_key import (
    ComponentsschemasProjectInputBeanProjectTemplateKey,
)
from ..models.componentsschemas_project_input_bean_project_type_key import (
    ComponentsschemasProjectInputBeanProjectTypeKey,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectInputBean")


@attr.s(auto_attribs=True)
class ProjectInputBean:
    """  """

    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    project_type_key: Union[Unset, ComponentsschemasProjectInputBeanProjectTypeKey] = UNSET
    project_template_key: Union[Unset, ComponentsschemasProjectInputBeanProjectTemplateKey] = UNSET
    description: Union[Unset, str] = UNSET
    lead: Union[Unset, str] = UNSET
    lead_account_id: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    assignee_type: Union[Unset, ComponentsschemasProjectInputBeanAssigneeType] = UNSET
    avatar_id: Union[Unset, int] = UNSET
    issue_security_scheme: Union[Unset, int] = UNSET
    permission_scheme: Union[Unset, int] = UNSET
    notification_scheme: Union[Unset, int] = UNSET
    category_id: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        name = self.name
        project_type_key: Union[Unset, str] = UNSET
        if not isinstance(self.project_type_key, Unset):
            project_type_key = self.project_type_key.value

        project_template_key: Union[Unset, str] = UNSET
        if not isinstance(self.project_template_key, Unset):
            project_template_key = self.project_template_key.value

        description = self.description
        lead = self.lead
        lead_account_id = self.lead_account_id
        url = self.url
        assignee_type: Union[Unset, str] = UNSET
        if not isinstance(self.assignee_type, Unset):
            assignee_type = self.assignee_type.value

        avatar_id = self.avatar_id
        issue_security_scheme = self.issue_security_scheme
        permission_scheme = self.permission_scheme
        notification_scheme = self.notification_scheme
        category_id = self.category_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if project_type_key is not UNSET:
            field_dict["projectTypeKey"] = project_type_key
        if project_template_key is not UNSET:
            field_dict["projectTemplateKey"] = project_template_key
        if description is not UNSET:
            field_dict["description"] = description
        if lead is not UNSET:
            field_dict["lead"] = lead
        if lead_account_id is not UNSET:
            field_dict["leadAccountId"] = lead_account_id
        if url is not UNSET:
            field_dict["url"] = url
        if assignee_type is not UNSET:
            field_dict["assigneeType"] = assignee_type
        if avatar_id is not UNSET:
            field_dict["avatarId"] = avatar_id
        if issue_security_scheme is not UNSET:
            field_dict["issueSecurityScheme"] = issue_security_scheme
        if permission_scheme is not UNSET:
            field_dict["permissionScheme"] = permission_scheme
        if notification_scheme is not UNSET:
            field_dict["notificationScheme"] = notification_scheme
        if category_id is not UNSET:
            field_dict["categoryId"] = category_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        project_type_key: Union[Unset, ComponentsschemasProjectInputBeanProjectTypeKey] = UNSET
        _project_type_key = d.pop("projectTypeKey", UNSET)
        if not isinstance(_project_type_key, Unset):
            project_type_key = ComponentsschemasProjectInputBeanProjectTypeKey(_project_type_key)

        project_template_key: Union[Unset, ComponentsschemasProjectInputBeanProjectTemplateKey] = UNSET
        _project_template_key = d.pop("projectTemplateKey", UNSET)
        if not isinstance(_project_template_key, Unset):
            project_template_key = ComponentsschemasProjectInputBeanProjectTemplateKey(_project_template_key)

        description = d.pop("description", UNSET)

        lead = d.pop("lead", UNSET)

        lead_account_id = d.pop("leadAccountId", UNSET)

        url = d.pop("url", UNSET)

        assignee_type: Union[Unset, ComponentsschemasProjectInputBeanAssigneeType] = UNSET
        _assignee_type = d.pop("assigneeType", UNSET)
        if not isinstance(_assignee_type, Unset):
            assignee_type = ComponentsschemasProjectInputBeanAssigneeType(_assignee_type)

        avatar_id = d.pop("avatarId", UNSET)

        issue_security_scheme = d.pop("issueSecurityScheme", UNSET)

        permission_scheme = d.pop("permissionScheme", UNSET)

        notification_scheme = d.pop("notificationScheme", UNSET)

        category_id = d.pop("categoryId", UNSET)

        project_input_bean = cls(
            key=key,
            name=name,
            project_type_key=project_type_key,
            project_template_key=project_template_key,
            description=description,
            lead=lead,
            lead_account_id=lead_account_id,
            url=url,
            assignee_type=assignee_type,
            avatar_id=avatar_id,
            issue_security_scheme=issue_security_scheme,
            permission_scheme=permission_scheme,
            notification_scheme=notification_scheme,
            category_id=category_id,
        )

        return project_input_bean
