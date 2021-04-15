from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="JiraExpressionsComplexityValueBean")


@attr.s(auto_attribs=True)
class JiraExpressionsComplexityValueBean:
    """  """

    value: int
    limit: int

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        limit = self.limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
                "limit": limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        limit = d.pop("limit")

        jira_expressions_complexity_value_bean = cls(
            value=value,
            limit=limit,
        )

        return jira_expressions_complexity_value_bean
