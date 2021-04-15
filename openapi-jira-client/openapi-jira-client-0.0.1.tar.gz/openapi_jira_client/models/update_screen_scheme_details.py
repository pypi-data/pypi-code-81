from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.update_screen_types import UpdateScreenTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateScreenSchemeDetails")


@attr.s(auto_attribs=True)
class UpdateScreenSchemeDetails:
    """ Details of a screen scheme. """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    screens: Union[Unset, UpdateScreenTypes] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        screens: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.screens, Unset):
            screens = self.screens.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if screens is not UNSET:
            field_dict["screens"] = screens

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        screens: Union[Unset, UpdateScreenTypes] = UNSET
        _screens = d.pop("screens", UNSET)
        if not isinstance(_screens, Unset):
            screens = UpdateScreenTypes.from_dict(_screens)

        update_screen_scheme_details = cls(
            name=name,
            description=description,
            screens=screens,
        )

        return update_screen_scheme_details
