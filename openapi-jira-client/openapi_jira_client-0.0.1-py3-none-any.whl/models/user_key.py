from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserKey")


@attr.s(auto_attribs=True)
class UserKey:
    """ List of user account IDs. """

    key: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        account_id = self.account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if account_id is not UNSET:
            field_dict["accountId"] = account_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        account_id = d.pop("accountId", UNSET)

        user_key = cls(
            key=key,
            account_id=account_id,
        )

        return user_key
