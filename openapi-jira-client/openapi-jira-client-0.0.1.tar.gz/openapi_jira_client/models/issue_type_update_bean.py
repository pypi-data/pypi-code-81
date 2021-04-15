from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeUpdateBean")


@attr.s(auto_attribs=True)
class IssueTypeUpdateBean:
    """  """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    avatar_id: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        avatar_id = self.avatar_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if avatar_id is not UNSET:
            field_dict["avatarId"] = avatar_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        avatar_id = d.pop("avatarId", UNSET)

        issue_type_update_bean = cls(
            name=name,
            description=description,
            avatar_id=avatar_id,
        )

        return issue_type_update_bean
