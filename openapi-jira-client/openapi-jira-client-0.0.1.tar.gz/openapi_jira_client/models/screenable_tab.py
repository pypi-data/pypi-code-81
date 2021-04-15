from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScreenableTab")


@attr.s(auto_attribs=True)
class ScreenableTab:
    """ A screen tab. """

    name: str
    id_: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id_ = self.id_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if id_ is not UNSET:
            field_dict["id"] = id_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id_ = d.pop("id", UNSET)

        screenable_tab = cls(
            name=name,
            id_=id_,
        )

        return screenable_tab
