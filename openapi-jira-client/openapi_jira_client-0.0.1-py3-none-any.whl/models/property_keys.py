from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.property_key import PropertyKey
from ..types import UNSET, Unset

T = TypeVar("T", bound="PropertyKeys")


@attr.s(auto_attribs=True)
class PropertyKeys:
    """ List of property keys. """

    keys: Union[Unset, List[PropertyKey]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        keys: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.keys, Unset):
            keys = []
            for keys_item_data in self.keys:
                keys_item = keys_item_data.to_dict()

                keys.append(keys_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if keys is not UNSET:
            field_dict["keys"] = keys

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        keys = []
        _keys = d.pop("keys", UNSET)
        for keys_item_data in _keys or []:
            keys_item = PropertyKey.from_dict(keys_item_data)

            keys.append(keys_item)

        property_keys = cls(
            keys=keys,
        )

        return property_keys
