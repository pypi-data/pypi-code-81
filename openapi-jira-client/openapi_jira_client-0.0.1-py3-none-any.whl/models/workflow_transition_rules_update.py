from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow_transition_rules import WorkflowTransitionRules

T = TypeVar("T", bound="WorkflowTransitionRulesUpdate")


@attr.s(auto_attribs=True)
class WorkflowTransitionRulesUpdate:
    """ Details about a workflow configuration update request. """

    workflows: List[WorkflowTransitionRules]

    def to_dict(self) -> Dict[str, Any]:
        workflows = []
        for workflows_item_data in self.workflows:
            workflows_item = workflows_item_data.to_dict()

            workflows.append(workflows_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflows": workflows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflows = []
        _workflows = d.pop("workflows")
        for workflows_item_data in _workflows:
            workflows_item = WorkflowTransitionRules.from_dict(workflows_item_data)

            workflows.append(workflows_item)

        workflow_transition_rules_update = cls(
            workflows=workflows,
        )

        return workflow_transition_rules_update
