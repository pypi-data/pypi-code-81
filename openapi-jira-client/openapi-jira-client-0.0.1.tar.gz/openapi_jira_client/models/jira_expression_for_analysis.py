from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_jira_expression_for_analysis_context_variables import (
    ComponentsschemasJiraExpressionForAnalysisContextVariables,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionForAnalysis")


@attr.s(auto_attribs=True)
class JiraExpressionForAnalysis:
    """ Details of Jira expressions for analysis. """

    expressions: List[str]
    context_variables: Union[Unset, ComponentsschemasJiraExpressionForAnalysisContextVariables] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expressions = self.expressions

        context_variables: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context_variables, Unset):
            context_variables = self.context_variables.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expressions": expressions,
            }
        )
        if context_variables is not UNSET:
            field_dict["contextVariables"] = context_variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expressions = cast(List[str], d.pop("expressions"))

        context_variables: Union[Unset, ComponentsschemasJiraExpressionForAnalysisContextVariables] = UNSET
        _context_variables = d.pop("contextVariables", UNSET)
        if not isinstance(_context_variables, Unset):
            context_variables = ComponentsschemasJiraExpressionForAnalysisContextVariables.from_dict(_context_variables)

        jira_expression_for_analysis = cls(
            expressions=expressions,
            context_variables=context_variables,
        )

        return jira_expression_for_analysis
