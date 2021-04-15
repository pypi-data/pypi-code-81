from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserMigrationBean")


@attr.s(auto_attribs=True)
class UserMigrationBean:
    """  """

    key: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        username = self.username
        account_id = self.account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if username is not UNSET:
            field_dict["username"] = username
        if account_id is not UNSET:
            field_dict["accountId"] = account_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        username = d.pop("username", UNSET)

        account_id = d.pop("accountId", UNSET)

        user_migration_bean = cls(
            key=key,
            username=username,
            account_id=account_id,
        )

        return user_migration_bean
