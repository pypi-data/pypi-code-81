from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.found_groups import FoundGroups
from ..models.found_users import FoundUsers
from ..types import UNSET, Unset

T = TypeVar("T", bound="FoundUsersAndGroups")


@attr.s(auto_attribs=True)
class FoundUsersAndGroups:
    """ List of users and groups found in a search. """

    users: Union[Unset, FoundUsers] = UNSET
    groups: Union[Unset, FoundGroups] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        users: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users.to_dict()

        groups: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if users is not UNSET:
            field_dict["users"] = users
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        users: Union[Unset, FoundUsers] = UNSET
        _users = d.pop("users", UNSET)
        if not isinstance(_users, Unset):
            users = FoundUsers.from_dict(_users)

        groups: Union[Unset, FoundGroups] = UNSET
        _groups = d.pop("groups", UNSET)
        if not isinstance(_groups, Unset):
            groups = FoundGroups.from_dict(_groups)

        found_users_and_groups = cls(
            users=users,
            groups=groups,
        )

        return found_users_and_groups
