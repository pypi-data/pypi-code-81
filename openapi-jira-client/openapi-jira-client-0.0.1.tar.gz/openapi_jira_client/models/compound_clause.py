from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_compound_clause_operator import ComponentsschemasCompoundClauseOperator
from ..models.jql_query_clause import JqlQueryClause

T = TypeVar("T", bound="CompoundClause")


@attr.s(auto_attribs=True)
class CompoundClause:
    """ A JQL query clause that consists of nested clauses. For example, `(labels in (urgent, blocker) OR lastCommentedBy = currentUser()). Note that, where nesting is not defined, the parser nests JQL clauses based on the operator precedence. For example, "A OR B AND C" is parsed as "(A OR B) AND C". See Setting the precedence of operators for more information about precedence in JQL queries.` """

    clauses: List[JqlQueryClause]
    operator: ComponentsschemasCompoundClauseOperator
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        clauses = []
        for clauses_item_data in self.clauses:
            clauses_item = clauses_item_data.to_dict()

            clauses.append(clauses_item)

        operator = self.operator.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "clauses": clauses,
                "operator": operator,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        clauses = []
        _clauses = d.pop("clauses")
        for clauses_item_data in _clauses:
            clauses_item = JqlQueryClause.from_dict(clauses_item_data)

            clauses.append(clauses_item)

        operator = ComponentsschemasCompoundClauseOperator(d.pop("operator"))

        compound_clause = cls(
            clauses=clauses,
            operator=operator,
        )

        compound_clause.additional_properties = d
        return compound_clause

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
