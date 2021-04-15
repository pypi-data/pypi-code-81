from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.paged_list_user_details_application_user import PagedListUserDetailsApplicationUser
from ..types import UNSET, Unset

T = TypeVar("T", bound="Group")


@attr.s(auto_attribs=True)
class Group:
    """  """

    name: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    users: Union[Unset, PagedListUserDetailsApplicationUser] = UNSET
    expand: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        self_ = self.self_
        users: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users.to_dict()

        expand = self.expand

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if self_ is not UNSET:
            field_dict["self"] = self_
        if users is not UNSET:
            field_dict["users"] = users
        if expand is not UNSET:
            field_dict["expand"] = expand

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        self_ = d.pop("self", UNSET)

        users: Union[Unset, PagedListUserDetailsApplicationUser] = UNSET
        _users = d.pop("users", UNSET)
        if not isinstance(_users, Unset):
            users = PagedListUserDetailsApplicationUser.from_dict(_users)

        expand = d.pop("expand", UNSET)

        group = cls(
            name=name,
            self_=self_,
            users=users,
            expand=expand,
        )

        return group
