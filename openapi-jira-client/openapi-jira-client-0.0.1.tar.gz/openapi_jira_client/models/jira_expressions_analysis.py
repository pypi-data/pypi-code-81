from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.jira_expression_analysis import JiraExpressionAnalysis

T = TypeVar("T", bound="JiraExpressionsAnalysis")


@attr.s(auto_attribs=True)
class JiraExpressionsAnalysis:
    """ Details about the analysed Jira expression. """

    results: List[JiraExpressionAnalysis]

    def to_dict(self) -> Dict[str, Any]:
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = JiraExpressionAnalysis.from_dict(results_item_data)

            results.append(results_item)

        jira_expressions_analysis = cls(
            results=results,
        )

        return jira_expressions_analysis
