from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRoleUser")


@attr.s(auto_attribs=True)
class ProjectRoleUser:
    """ Details of the user associated with the role. """

    account_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["accountId"] = account_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        project_role_user = cls(
            account_id=account_id,
        )

        return project_role_user
