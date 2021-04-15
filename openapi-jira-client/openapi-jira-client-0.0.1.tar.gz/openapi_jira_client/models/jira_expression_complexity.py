from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_jira_expression_complexity_variables import (
    ComponentsschemasJiraExpressionComplexityVariables,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionComplexity")


@attr.s(auto_attribs=True)
class JiraExpressionComplexity:
    """ Details about the complexity of the analysed Jira expression. """

    expensive_operations: str
    variables: Union[Unset, ComponentsschemasJiraExpressionComplexityVariables] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expensive_operations = self.expensive_operations
        variables: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expensiveOperations": expensive_operations,
            }
        )
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expensive_operations = d.pop("expensiveOperations")

        variables: Union[Unset, ComponentsschemasJiraExpressionComplexityVariables] = UNSET
        _variables = d.pop("variables", UNSET)
        if not isinstance(_variables, Unset):
            variables = ComponentsschemasJiraExpressionComplexityVariables.from_dict(_variables)

        jira_expression_complexity = cls(
            expensive_operations=expensive_operations,
            variables=variables,
        )

        return jira_expression_complexity
