from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.avatar import Avatar
from ..types import UNSET, Unset

T = TypeVar("T", bound="SystemAvatars")


@attr.s(auto_attribs=True)
class SystemAvatars:
    """ List of system avatars. """

    system: Union[Unset, List[Avatar]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        system: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.system, Unset):
            system = []
            for system_item_data in self.system:
                system_item = system_item_data.to_dict()

                system.append(system_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if system is not UNSET:
            field_dict["system"] = system

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        system = []
        _system = d.pop("system", UNSET)
        for system_item_data in _system or []:
            system_item = Avatar.from_dict(system_item_data)

            system.append(system_item)

        system_avatars = cls(
            system=system,
        )

        return system_avatars
