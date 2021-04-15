from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_field_value_clause_operator import ComponentsschemasFieldValueClauseOperator
from ..models.jql_query_clause_operand import JqlQueryClauseOperand
from ..models.jql_query_field import JqlQueryField

T = TypeVar("T", bound="FieldValueClause")


@attr.s(auto_attribs=True)
class FieldValueClause:
    """ A clause that asserts the current value of a field. For example, `summary ~ test`. """

    field: JqlQueryField
    operator: ComponentsschemasFieldValueClauseOperator
    operand: JqlQueryClauseOperand
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field = self.field.to_dict()

        operator = self.operator.value

        operand = self.operand.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "operator": operator,
                "operand": operand,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = JqlQueryField.from_dict(d.pop("field"))

        operator = ComponentsschemasFieldValueClauseOperator(d.pop("operator"))

        operand = JqlQueryClauseOperand.from_dict(d.pop("operand"))

        field_value_clause = cls(
            field=field,
            operator=operator,
            operand=operand,
        )

        field_value_clause.additional_properties = d
        return field_value_clause

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
