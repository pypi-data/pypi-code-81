from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user_picker_user import UserPickerUser
from ..types import UNSET, Unset

T = TypeVar("T", bound="FoundUsers")


@attr.s(auto_attribs=True)
class FoundUsers:
    """ The list of users found in a search, including header text (Showing X of Y matching users) and total of matched users. """

    users: Union[Unset, List[UserPickerUser]] = UNSET
    total: Union[Unset, int] = UNSET
    header: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()

                users.append(users_item)

        total = self.total
        header = self.header

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if users is not UNSET:
            field_dict["users"] = users
        if total is not UNSET:
            field_dict["total"] = total
        if header is not UNSET:
            field_dict["header"] = header

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = UserPickerUser.from_dict(users_item_data)

            users.append(users_item)

        total = d.pop("total", UNSET)

        header = d.pop("header", UNSET)

        found_users = cls(
            users=users,
            total=total,
            header=header,
        )

        return found_users
