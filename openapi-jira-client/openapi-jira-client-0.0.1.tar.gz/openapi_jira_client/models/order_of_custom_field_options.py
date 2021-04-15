from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_order_of_custom_field_options_position import (
    ComponentsschemasOrderOfCustomFieldOptionsPosition,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderOfCustomFieldOptions")


@attr.s(auto_attribs=True)
class OrderOfCustomFieldOptions:
    """ An ordered list of custom field option IDs and information on where to move them. """

    custom_field_option_ids: List[str]
    after: Union[Unset, str] = UNSET
    position: Union[Unset, ComponentsschemasOrderOfCustomFieldOptionsPosition] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        custom_field_option_ids = self.custom_field_option_ids

        after = self.after
        position: Union[Unset, str] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "customFieldOptionIds": custom_field_option_ids,
            }
        )
        if after is not UNSET:
            field_dict["after"] = after
        if position is not UNSET:
            field_dict["position"] = position

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_field_option_ids = cast(List[str], d.pop("customFieldOptionIds"))

        after = d.pop("after", UNSET)

        position: Union[Unset, ComponentsschemasOrderOfCustomFieldOptionsPosition] = UNSET
        _position = d.pop("position", UNSET)
        if not isinstance(_position, Unset):
            position = ComponentsschemasOrderOfCustomFieldOptionsPosition(_position)

        order_of_custom_field_options = cls(
            custom_field_option_ids=custom_field_option_ids,
            after=after,
            position=position,
        )

        return order_of_custom_field_options
