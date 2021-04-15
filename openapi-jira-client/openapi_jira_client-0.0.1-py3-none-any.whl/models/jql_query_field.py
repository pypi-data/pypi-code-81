from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.jql_query_field_entity_property import JqlQueryFieldEntityProperty
from ..types import UNSET, Unset

T = TypeVar("T", bound="JqlQueryField")


@attr.s(auto_attribs=True)
class JqlQueryField:
    """ A field used in a JQL query. See [Advanced searching - fields reference](https://confluence.atlassian.com/x/dAiiLQ) for more information about fields in JQL queries. """

    name: str
    property_: Union[Unset, List[JqlQueryFieldEntityProperty]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        property_: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.property_, Unset):
            property_ = []
            for property_item_data in self.property_:
                property_item = property_item_data.to_dict()

                property_.append(property_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if property_ is not UNSET:
            field_dict["property"] = property_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        property_ = []
        _property_ = d.pop("property", UNSET)
        for property_item_data in _property_ or []:
            property_item = JqlQueryFieldEntityProperty.from_dict(property_item_data)

            property_.append(property_item)

        jql_query_field = cls(
            name=name,
            property_=property_,
        )

        return jql_query_field
