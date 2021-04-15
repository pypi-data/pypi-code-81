from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_jira_expression_validation_error_type import (
    ComponentsschemasJiraExpressionValidationErrorType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionValidationError")


@attr.s(auto_attribs=True)
class JiraExpressionValidationError:
    """Details about syntax and type errors. The error details apply to the entire expression, unless the object includes:

    *  `line` and `column`
    *  `expression`"""

    message: str
    type_: ComponentsschemasJiraExpressionValidationErrorType
    line: Union[Unset, int] = UNSET
    column: Union[Unset, int] = UNSET
    expression: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        type_ = self.type_.value

        line = self.line
        column = self.column
        expression = self.expression

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "message": message,
                "type": type_,
            }
        )
        if line is not UNSET:
            field_dict["line"] = line
        if column is not UNSET:
            field_dict["column"] = column
        if expression is not UNSET:
            field_dict["expression"] = expression

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        type_ = ComponentsschemasJiraExpressionValidationErrorType(d.pop("type"))

        line = d.pop("line", UNSET)

        column = d.pop("column", UNSET)

        expression = d.pop("expression", UNSET)

        jira_expression_validation_error = cls(
            message=message,
            type_=type_,
            line=line,
            column=column,
            expression=expression,
        )

        return jira_expression_validation_error
