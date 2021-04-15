from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldConfigurationItem")


@attr.s(auto_attribs=True)
class FieldConfigurationItem:
    """ A field within a field configuration. """

    id_: str
    description: Union[Unset, str] = UNSET
    is_hidden: Union[Unset, bool] = UNSET
    is_required: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        description = self.description
        is_hidden = self.is_hidden
        is_required = self.is_required

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if is_hidden is not UNSET:
            field_dict["isHidden"] = is_hidden
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        description = d.pop("description", UNSET)

        is_hidden = d.pop("isHidden", UNSET)

        is_required = d.pop("isRequired", UNSET)

        field_configuration_item = cls(
            id_=id_,
            description=description,
            is_hidden=is_hidden,
            is_required=is_required,
        )

        return field_configuration_item
