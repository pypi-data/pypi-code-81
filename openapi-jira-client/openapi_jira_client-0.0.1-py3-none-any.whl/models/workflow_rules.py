from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.workflow_condition_bean import WorkflowConditionBean
from ..models.workflow_transition_rule import WorkflowTransitionRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowRules")


@attr.s(auto_attribs=True)
class WorkflowRules:
    """ A collection of transition rules. """

    conditions: List[WorkflowTransitionRule]
    validators: List[WorkflowTransitionRule]
    post_functions: List[WorkflowTransitionRule]
    conditions_tree: Union[Unset, WorkflowConditionBean] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()

            conditions.append(conditions_item)

        validators = []
        for validators_item_data in self.validators:
            validators_item = validators_item_data.to_dict()

            validators.append(validators_item)

        post_functions = []
        for post_functions_item_data in self.post_functions:
            post_functions_item = post_functions_item_data.to_dict()

            post_functions.append(post_functions_item)

        conditions_tree: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.conditions_tree, Unset):
            conditions_tree = self.conditions_tree.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "conditions": conditions,
                "validators": validators,
                "postFunctions": post_functions,
            }
        )
        if conditions_tree is not UNSET:
            field_dict["conditionsTree"] = conditions_tree

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = WorkflowTransitionRule.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        validators = []
        _validators = d.pop("validators")
        for validators_item_data in _validators:
            validators_item = WorkflowTransitionRule.from_dict(validators_item_data)

            validators.append(validators_item)

        post_functions = []
        _post_functions = d.pop("postFunctions")
        for post_functions_item_data in _post_functions:
            post_functions_item = WorkflowTransitionRule.from_dict(post_functions_item_data)

            post_functions.append(post_functions_item)

        conditions_tree: Union[Unset, WorkflowConditionBean] = UNSET
        _conditions_tree = d.pop("conditionsTree", UNSET)
        if not isinstance(_conditions_tree, Unset):
            conditions_tree = WorkflowConditionBean.from_dict(_conditions_tree)

        workflow_rules = cls(
            conditions=conditions,
            validators=validators,
            post_functions=post_functions,
            conditions_tree=conditions_tree,
        )

        return workflow_rules
