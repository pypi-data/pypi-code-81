from typing import Any, Dict, Type, TypeVar

import attr

from ..models.jira_expressions_complexity_value_bean import JiraExpressionsComplexityValueBean

T = TypeVar("T", bound="JiraExpressionsComplexityBean")


@attr.s(auto_attribs=True)
class JiraExpressionsComplexityBean:
    """  """

    steps: JiraExpressionsComplexityValueBean
    expensive_operations: JiraExpressionsComplexityValueBean
    beans: JiraExpressionsComplexityValueBean
    primitive_values: JiraExpressionsComplexityValueBean

    def to_dict(self) -> Dict[str, Any]:
        steps = self.steps.to_dict()

        expensive_operations = self.expensive_operations.to_dict()

        beans = self.beans.to_dict()

        primitive_values = self.primitive_values.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "steps": steps,
                "expensiveOperations": expensive_operations,
                "beans": beans,
                "primitiveValues": primitive_values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        steps = JiraExpressionsComplexityValueBean.from_dict(d.pop("steps"))

        expensive_operations = JiraExpressionsComplexityValueBean.from_dict(d.pop("expensiveOperations"))

        beans = JiraExpressionsComplexityValueBean.from_dict(d.pop("beans"))

        primitive_values = JiraExpressionsComplexityValueBean.from_dict(d.pop("primitiveValues"))

        jira_expressions_complexity_bean = cls(
            steps=steps,
            expensive_operations=expensive_operations,
            beans=beans,
            primitive_values=primitive_values,
        )

        return jira_expressions_complexity_bean
