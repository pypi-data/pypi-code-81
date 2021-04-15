from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.connect_workflow_transition_rule import ConnectWorkflowTransitionRule
from ..models.workflow_id import WorkflowId

T = TypeVar("T", bound="WorkflowTransitionRules")


@attr.s(auto_attribs=True)
class WorkflowTransitionRules:
    """ A workflow with transition rules. """

    workflow_id: WorkflowId
    post_functions: List[ConnectWorkflowTransitionRule]
    conditions: List[ConnectWorkflowTransitionRule]
    validators: List[ConnectWorkflowTransitionRule]

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id.to_dict()

        post_functions = []
        for post_functions_item_data in self.post_functions:
            post_functions_item = post_functions_item_data.to_dict()

            post_functions.append(post_functions_item)

        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()

            conditions.append(conditions_item)

        validators = []
        for validators_item_data in self.validators:
            validators_item = validators_item_data.to_dict()

            validators.append(validators_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflowId": workflow_id,
                "postFunctions": post_functions,
                "conditions": conditions,
                "validators": validators,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_id = WorkflowId.from_dict(d.pop("workflowId"))

        post_functions = []
        _post_functions = d.pop("postFunctions")
        for post_functions_item_data in _post_functions:
            post_functions_item = ConnectWorkflowTransitionRule.from_dict(post_functions_item_data)

            post_functions.append(post_functions_item)

        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = ConnectWorkflowTransitionRule.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        validators = []
        _validators = d.pop("validators")
        for validators_item_data in _validators:
            validators_item = ConnectWorkflowTransitionRule.from_dict(validators_item_data)

            validators.append(validators_item)

        workflow_transition_rules = cls(
            workflow_id=workflow_id,
            post_functions=post_functions,
            conditions=conditions,
            validators=validators,
        )

        return workflow_transition_rules
