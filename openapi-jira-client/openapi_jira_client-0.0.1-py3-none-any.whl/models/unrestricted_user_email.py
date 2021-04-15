from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnrestrictedUserEmail")


@attr.s(auto_attribs=True)
class UnrestrictedUserEmail:
    """  """

    account_id: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        email = d.pop("email", UNSET)

        unrestricted_user_email = cls(
            account_id=account_id,
            email=email,
        )

        return unrestricted_user_email
