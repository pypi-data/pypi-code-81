from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeInfo")


@attr.s(auto_attribs=True)
class IssueTypeInfo:
    """ Details of an issue type. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    avatar_id: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        avatar_id = self.avatar_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if avatar_id is not UNSET:
            field_dict["avatarId"] = avatar_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        avatar_id = d.pop("avatarId", UNSET)

        issue_type_info = cls(
            id_=id_,
            name=name,
            avatar_id=avatar_id,
        )

        return issue_type_info
