from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.avatar import Avatar
from ..types import UNSET, Unset

T = TypeVar("T", bound="Avatars")


@attr.s(auto_attribs=True)
class Avatars:
    """ Details about system and custom avatars. """

    system: Union[Unset, List[Avatar]] = UNSET
    custom: Union[Unset, List[Avatar]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        system: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.system, Unset):
            system = []
            for system_item_data in self.system:
                system_item = system_item_data.to_dict()

                system.append(system_item)

        custom: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.custom, Unset):
            custom = []
            for custom_item_data in self.custom:
                custom_item = custom_item_data.to_dict()

                custom.append(custom_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if system is not UNSET:
            field_dict["system"] = system
        if custom is not UNSET:
            field_dict["custom"] = custom

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        system = []
        _system = d.pop("system", UNSET)
        for system_item_data in _system or []:
            system_item = Avatar.from_dict(system_item_data)

            system.append(system_item)

        custom = []
        _custom = d.pop("custom", UNSET)
        for custom_item_data in _custom or []:
            custom_item = Avatar.from_dict(custom_item_data)

            custom.append(custom_item)

        avatars = cls(
            system=system,
            custom=custom,
        )

        return avatars
