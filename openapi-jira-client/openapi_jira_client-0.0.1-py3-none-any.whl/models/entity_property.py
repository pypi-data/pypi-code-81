from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntityProperty")


@attr.s(auto_attribs=True)
class EntityProperty:
    """ An entity property, for more information see [Entity properties](https://developer.atlassian.com/cloud/jira/platform/jira-entity-properties/). """

    key: Union[Unset, str] = UNSET
    value: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        value = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        value = None

        entity_property = cls(
            key=key,
            value=value,
        )

        return entity_property
