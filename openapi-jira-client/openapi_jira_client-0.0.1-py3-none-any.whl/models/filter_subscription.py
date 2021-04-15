from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.group_name import GroupName
from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterSubscription")


@attr.s(auto_attribs=True)
class FilterSubscription:
    """ Details of a user or group subscribing to a filter. """

    id_: Union[Unset, int] = UNSET
    user: Union[Unset, User] = UNSET
    group: Union[Unset, GroupName] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.group, Unset):
            group = self.group.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if user is not UNSET:
            field_dict["user"] = user
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        user: Union[Unset, User] = UNSET
        _user = d.pop("user", UNSET)
        if not isinstance(_user, Unset):
            user = User.from_dict(_user)

        group: Union[Unset, GroupName] = UNSET
        _group = d.pop("group", UNSET)
        if not isinstance(_group, Unset):
            group = GroupName.from_dict(_group)

        filter_subscription = cls(
            id_=id_,
            user=user,
            group=group,
        )

        return filter_subscription
