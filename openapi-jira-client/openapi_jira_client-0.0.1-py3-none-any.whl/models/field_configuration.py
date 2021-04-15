from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldConfiguration")


@attr.s(auto_attribs=True)
class FieldConfiguration:
    """ Details of a field configuration. """

    id_: int
    name: str
    description: str
    is_default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
                "description": description,
            }
        )
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        is_default = d.pop("isDefault", UNSET)

        field_configuration = cls(
            id_=id_,
            name=name,
            description=description,
            is_default=is_default,
        )

        return field_configuration
