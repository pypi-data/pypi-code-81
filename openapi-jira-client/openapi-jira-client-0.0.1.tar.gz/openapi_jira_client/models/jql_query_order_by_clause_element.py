from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_jql_query_order_by_clause_element_direction import (
    ComponentsschemasJqlQueryOrderByClauseElementDirection,
)
from ..models.jql_query_field import JqlQueryField
from ..types import UNSET, Unset

T = TypeVar("T", bound="JqlQueryOrderByClauseElement")


@attr.s(auto_attribs=True)
class JqlQueryOrderByClauseElement:
    """ An element of the order-by JQL clause. """

    field: JqlQueryField
    direction: Union[Unset, ComponentsschemasJqlQueryOrderByClauseElementDirection] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field = self.field.to_dict()

        direction: Union[Unset, str] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "field": field,
            }
        )
        if direction is not UNSET:
            field_dict["direction"] = direction

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = JqlQueryField.from_dict(d.pop("field"))

        direction: Union[Unset, ComponentsschemasJqlQueryOrderByClauseElementDirection] = UNSET
        _direction = d.pop("direction", UNSET)
        if not isinstance(_direction, Unset):
            direction = ComponentsschemasJqlQueryOrderByClauseElementDirection(_direction)

        jql_query_order_by_clause_element = cls(
            field=field,
            direction=direction,
        )

        return jql_query_order_by_clause_element
