from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="Context")


@attr.s(auto_attribs=True)
class Context:
    """ A context. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    scope: Union[Unset, Scope] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        scope: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        scope: Union[Unset, Scope] = UNSET
        _scope = d.pop("scope", UNSET)
        if not isinstance(_scope, Unset):
            scope = Scope.from_dict(_scope)

        context = cls(
            id_=id_,
            name=name,
            scope=scope,
        )

        return context
