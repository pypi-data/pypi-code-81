from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.jira_expression_evaluation_meta_data_bean import JiraExpressionEvaluationMetaDataBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="JiraExpressionResult")


@attr.s(auto_attribs=True)
class JiraExpressionResult:
    """ The result of evaluating a Jira expression. """

    value: None
    meta: Union[Unset, JiraExpressionEvaluationMetaDataBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = None

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = None

        meta: Union[Unset, JiraExpressionEvaluationMetaDataBean] = UNSET
        _meta = d.pop("meta", UNSET)
        if not isinstance(_meta, Unset):
            meta = JiraExpressionEvaluationMetaDataBean.from_dict(_meta)

        jira_expression_result = cls(
            value=value,
            meta=meta,
        )

        return jira_expression_result
