from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_event_notification_notification_type import (
    ComponentsschemasEventNotificationNotificationType,
)
from ..models.field_details import FieldDetails
from ..models.group_name import GroupName
from ..models.project_role import ProjectRole
from ..models.user_details import UserDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="EventNotification")


@attr.s(auto_attribs=True)
class EventNotification:
    """ Details about a notification associated with an event. """

    expand: Union[Unset, str] = UNSET
    id_: Union[Unset, int] = UNSET
    notification_type: Union[Unset, ComponentsschemasEventNotificationNotificationType] = UNSET
    parameter: Union[Unset, str] = UNSET
    group: Union[Unset, GroupName] = UNSET
    field: Union[Unset, FieldDetails] = UNSET
    email_address: Union[Unset, str] = UNSET
    project_role: Union[Unset, ProjectRole] = UNSET
    user: Union[Unset, UserDetails] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        id_ = self.id_
        notification_type: Union[Unset, str] = UNSET
        if not isinstance(self.notification_type, Unset):
            notification_type = self.notification_type.value

        parameter = self.parameter
        group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.group, Unset):
            group = self.group.to_dict()

        field: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field, Unset):
            field = self.field.to_dict()

        email_address = self.email_address
        project_role: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.project_role, Unset):
            project_role = self.project_role.to_dict()

        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if id_ is not UNSET:
            field_dict["id"] = id_
        if notification_type is not UNSET:
            field_dict["notificationType"] = notification_type
        if parameter is not UNSET:
            field_dict["parameter"] = parameter
        if group is not UNSET:
            field_dict["group"] = group
        if field is not UNSET:
            field_dict["field"] = field
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if project_role is not UNSET:
            field_dict["projectRole"] = project_role
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        id_ = d.pop("id", UNSET)

        notification_type: Union[Unset, ComponentsschemasEventNotificationNotificationType] = UNSET
        _notification_type = d.pop("notificationType", UNSET)
        if not isinstance(_notification_type, Unset):
            notification_type = ComponentsschemasEventNotificationNotificationType(_notification_type)

        parameter = d.pop("parameter", UNSET)

        group: Union[Unset, GroupName] = UNSET
        _group = d.pop("group", UNSET)
        if not isinstance(_group, Unset):
            group = GroupName.from_dict(_group)

        field: Union[Unset, FieldDetails] = UNSET
        _field = d.pop("field", UNSET)
        if not isinstance(_field, Unset):
            field = FieldDetails.from_dict(_field)

        email_address = d.pop("emailAddress", UNSET)

        project_role: Union[Unset, ProjectRole] = UNSET
        _project_role = d.pop("projectRole", UNSET)
        if not isinstance(_project_role, Unset):
            project_role = ProjectRole.from_dict(_project_role)

        user: Union[Unset, UserDetails] = UNSET
        _user = d.pop("user", UNSET)
        if not isinstance(_user, Unset):
            user = UserDetails.from_dict(_user)

        event_notification = cls(
            expand=expand,
            id_=id_,
            notification_type=notification_type,
            parameter=parameter,
            group=group,
            field=field,
            email_address=email_address,
            project_role=project_role,
            user=user,
        )

        return event_notification
