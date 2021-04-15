from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.jira_expression_eval_context_bean import JiraExpressionEvalContextBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionEvalRequestBean")


@attr.s(auto_attribs=True)
class JiraExpressionEvalRequestBean:
    """  """

    expression: str
    context: Union[Unset, JiraExpressionEvalContextBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expression = self.expression
        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expression": expression,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expression = d.pop("expression")

        context: Union[Unset, JiraExpressionEvalContextBean] = UNSET
        _context = d.pop("context", UNSET)
        if not isinstance(_context, Unset):
            context = JiraExpressionEvalContextBean.from_dict(_context)

        jira_expression_eval_request_bean = cls(
            expression=expression,
            context=context,
        )

        return jira_expression_eval_request_bean
