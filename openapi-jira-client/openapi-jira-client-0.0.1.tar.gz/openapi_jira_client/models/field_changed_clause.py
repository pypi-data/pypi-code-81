from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_field_changed_clause_operator import ComponentsschemasFieldChangedClauseOperator
from ..models.jql_query_clause_time_predicate import JqlQueryClauseTimePredicate
from ..models.jql_query_field import JqlQueryField

T = TypeVar("T", bound="FieldChangedClause")


@attr.s(auto_attribs=True)
class FieldChangedClause:
    """ A clause that asserts whether a field was changed. For example, `status CHANGED AFTER startOfMonth(-1M)`.See [CHANGED](https://confluence.atlassian.com/x/dgiiLQ#Advancedsearching-operatorsreference-CHANGEDCHANGED) for more information about the CHANGED operator. """

    field: JqlQueryField
    operator: ComponentsschemasFieldChangedClauseOperator
    predicates: List[JqlQueryClauseTimePredicate]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field = self.field.to_dict()

        operator = self.operator.value

        predicates = []
        for predicates_item_data in self.predicates:
            predicates_item = predicates_item_data.to_dict()

            predicates.append(predicates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "operator": operator,
                "predicates": predicates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field = JqlQueryField.from_dict(d.pop("field"))

        operator = ComponentsschemasFieldChangedClauseOperator(d.pop("operator"))

        predicates = []
        _predicates = d.pop("predicates")
        for predicates_item_data in _predicates:
            predicates_item = JqlQueryClauseTimePredicate.from_dict(predicates_item_data)

            predicates.append(predicates_item)

        field_changed_clause = cls(
            field=field,
            operator=operator,
            predicates=predicates,
        )

        field_changed_clause.additional_properties = d
        return field_changed_clause

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
