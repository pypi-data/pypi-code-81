from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatedProjectCategory")


@attr.s(auto_attribs=True)
class UpdatedProjectCategory:
    """ A project category. """

    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        description = self.description
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        updated_project_category = cls(
            self_=self_,
            id_=id_,
            description=description,
            name=name,
        )

        return updated_project_category
