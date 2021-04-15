from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectIdentifierBean")


@attr.s(auto_attribs=True)
class ProjectIdentifierBean:
    """ The identifiers for a project. """

    id_: Union[Unset, int] = UNSET
    key: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        project_identifier_bean = cls(
            id_=id_,
            key=key,
        )

        return project_identifier_bean
