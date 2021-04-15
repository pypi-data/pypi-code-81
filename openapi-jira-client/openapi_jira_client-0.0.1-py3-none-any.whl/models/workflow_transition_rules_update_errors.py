from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow_transition_rules_update_error_details import WorkflowTransitionRulesUpdateErrorDetails

T = TypeVar("T", bound="WorkflowTransitionRulesUpdateErrors")


@attr.s(auto_attribs=True)
class WorkflowTransitionRulesUpdateErrors:
    """ Details of any errors encountered while updating workflow transition rules. """

    update_results: List[WorkflowTransitionRulesUpdateErrorDetails]

    def to_dict(self) -> Dict[str, Any]:
        update_results = []
        for update_results_item_data in self.update_results:
            update_results_item = update_results_item_data.to_dict()

            update_results.append(update_results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "updateResults": update_results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        update_results = []
        _update_results = d.pop("updateResults")
        for update_results_item_data in _update_results:
            update_results_item = WorkflowTransitionRulesUpdateErrorDetails.from_dict(update_results_item_data)

            update_results.append(update_results_item)

        workflow_transition_rules_update_errors = cls(
            update_results=update_results,
        )

        return workflow_transition_rules_update_errors
