from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.group_name import GroupName
from ..models.restricted_permission import RestrictedPermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationRecipientsRestrictions")


@attr.s(auto_attribs=True)
class NotificationRecipientsRestrictions:
    """ Details of the group membership or permissions needed to receive the notification. """

    groups: Union[Unset, List[GroupName]] = UNSET
    permissions: Union[Unset, List[RestrictedPermission]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()

                permissions.append(permissions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if groups is not UNSET:
            field_dict["groups"] = groups
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = GroupName.from_dict(groups_item_data)

            groups.append(groups_item)

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = RestrictedPermission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        notification_recipients_restrictions = cls(
            groups=groups,
            permissions=permissions,
        )

        return notification_recipients_restrictions
