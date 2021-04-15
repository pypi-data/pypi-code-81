from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.issues_meta_bean import IssuesMetaBean
from ..models.jira_expressions_complexity_bean import JiraExpressionsComplexityBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionEvaluationMetaDataBean")


@attr.s(auto_attribs=True)
class JiraExpressionEvaluationMetaDataBean:
    """  """

    complexity: Union[Unset, JiraExpressionsComplexityBean] = UNSET
    issues: Union[Unset, IssuesMetaBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        complexity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.complexity, Unset):
            complexity = self.complexity.to_dict()

        issues: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = self.issues.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if complexity is not UNSET:
            field_dict["complexity"] = complexity
        if issues is not UNSET:
            field_dict["issues"] = issues

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        complexity: Union[Unset, JiraExpressionsComplexityBean] = UNSET
        _complexity = d.pop("complexity", UNSET)
        if not isinstance(_complexity, Unset):
            complexity = JiraExpressionsComplexityBean.from_dict(_complexity)

        issues: Union[Unset, IssuesMetaBean] = UNSET
        _issues = d.pop("issues", UNSET)
        if not isinstance(_issues, Unset):
            issues = IssuesMetaBean.from_dict(_issues)

        jira_expression_evaluation_meta_data_bean = cls(
            complexity=complexity,
            issues=issues,
        )

        return jira_expression_evaluation_meta_data_bean
