from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_jql_query_field_entity_property_type import (
    ComponentsschemasJqlQueryFieldEntityPropertyType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="JqlQueryFieldEntityProperty")


@attr.s(auto_attribs=True)
class JqlQueryFieldEntityProperty:
    """ Details of an entity property. """

    entity: str
    key: str
    path: str
    type_: Union[Unset, ComponentsschemasJqlQueryFieldEntityPropertyType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity = self.entity
        key = self.key
        path = self.path
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity": entity,
                "key": key,
                "path": path,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity = d.pop("entity")

        key = d.pop("key")

        path = d.pop("path")

        type_: Union[Unset, ComponentsschemasJqlQueryFieldEntityPropertyType] = UNSET
        _type_ = d.pop("type", UNSET)
        if not isinstance(_type_, Unset):
            type_ = ComponentsschemasJqlQueryFieldEntityPropertyType(_type_)

        jql_query_field_entity_property = cls(
            entity=entity,
            key=key,
            path=path,
            type_=type_,
        )

        jql_query_field_entity_property.additional_properties = d
        return jql_query_field_entity_property

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
