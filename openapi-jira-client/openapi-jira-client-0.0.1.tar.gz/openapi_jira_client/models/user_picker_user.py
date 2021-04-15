from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPickerUser")


@attr.s(auto_attribs=True)
class UserPickerUser:
    """ A user found in a search. """

    account_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    html: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    avatar_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        name = self.name
        key = self.key
        html = self.html
        display_name = self.display_name
        avatar_url = self.avatar_url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if name is not UNSET:
            field_dict["name"] = name
        if key is not UNSET:
            field_dict["key"] = key
        if html is not UNSET:
            field_dict["html"] = html
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if avatar_url is not UNSET:
            field_dict["avatarUrl"] = avatar_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        name = d.pop("name", UNSET)

        key = d.pop("key", UNSET)

        html = d.pop("html", UNSET)

        display_name = d.pop("displayName", UNSET)

        avatar_url = d.pop("avatarUrl", UNSET)

        user_picker_user = cls(
            account_id=account_id,
            name=name,
            key=key,
            html=html,
            display_name=display_name,
            avatar_url=avatar_url,
        )

        return user_picker_user
