from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_workflow_compound_condition_operator import (
    ComponentsschemasWorkflowCompoundConditionOperator,
)
from ..models.workflow_condition_bean import WorkflowConditionBean

T = TypeVar("T", bound="WorkflowCompoundCondition")


@attr.s(auto_attribs=True)
class WorkflowCompoundCondition:
    """ A workflow transition compound condition rule. """

    operator: ComponentsschemasWorkflowCompoundConditionOperator
    conditions: List[WorkflowConditionBean]
    node_type: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operator = self.operator.value

        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()

            conditions.append(conditions_item)

        node_type = self.node_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
                "conditions": conditions,
                "nodeType": node_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = ComponentsschemasWorkflowCompoundConditionOperator(d.pop("operator"))

        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = WorkflowConditionBean.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        node_type = d.pop("nodeType")

        workflow_compound_condition = cls(
            operator=operator,
            conditions=conditions,
            node_type=node_type,
        )

        workflow_compound_condition.additional_properties = d
        return workflow_compound_condition

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
