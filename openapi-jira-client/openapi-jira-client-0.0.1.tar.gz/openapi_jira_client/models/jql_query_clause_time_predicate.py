from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_jql_query_clause_time_predicate_operator import (
    ComponentsschemasJqlQueryClauseTimePredicateOperator,
)
from ..models.jql_query_clause_operand import JqlQueryClauseOperand

T = TypeVar("T", bound="JqlQueryClauseTimePredicate")


@attr.s(auto_attribs=True)
class JqlQueryClauseTimePredicate:
    """ A time predicate for a temporal JQL clause. """

    operator: ComponentsschemasJqlQueryClauseTimePredicateOperator
    operand: JqlQueryClauseOperand
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operator = self.operator.value

        operand = self.operand.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
                "operand": operand,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = ComponentsschemasJqlQueryClauseTimePredicateOperator(d.pop("operator"))

        operand = JqlQueryClauseOperand.from_dict(d.pop("operand"))

        jql_query_clause_time_predicate = cls(
            operator=operator,
            operand=operand,
        )

        jql_query_clause_time_predicate.additional_properties = d
        return jql_query_clause_time_predicate

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
