from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.jql_query_order_by_clause_element import JqlQueryOrderByClauseElement

T = TypeVar("T", bound="JqlQueryOrderByClause")


@attr.s(auto_attribs=True)
class JqlQueryOrderByClause:
    """ Details of the order-by JQL clause. """

    fields: List[JqlQueryOrderByClauseElement]

    def to_dict(self) -> Dict[str, Any]:
        fields = []
        for fields_item_data in self.fields:
            fields_item = fields_item_data.to_dict()

            fields.append(fields_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = []
        _fields = d.pop("fields")
        for fields_item_data in _fields:
            fields_item = JqlQueryOrderByClauseElement.from_dict(fields_item_data)

            fields.append(fields_item)

        jql_query_order_by_clause = cls(
            fields=fields,
        )

        return jql_query_order_by_clause
