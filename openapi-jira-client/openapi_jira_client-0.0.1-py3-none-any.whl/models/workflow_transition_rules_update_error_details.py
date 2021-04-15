from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.componentsschemas_workflow_transition_rules_update_error_details_rule_update_errors import (
    ComponentsschemasWorkflowTransitionRulesUpdateErrorDetailsRuleUpdateErrors,
)
from ..models.workflow_id import WorkflowId

T = TypeVar("T", bound="WorkflowTransitionRulesUpdateErrorDetails")


@attr.s(auto_attribs=True)
class WorkflowTransitionRulesUpdateErrorDetails:
    """ Details of any errors encountered while updating workflow transition rules for a workflow. """

    workflow_id: WorkflowId
    rule_update_errors: ComponentsschemasWorkflowTransitionRulesUpdateErrorDetailsRuleUpdateErrors
    update_errors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id.to_dict()

        rule_update_errors = self.rule_update_errors.to_dict()

        update_errors = self.update_errors

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflowId": workflow_id,
                "ruleUpdateErrors": rule_update_errors,
                "updateErrors": update_errors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow_id = WorkflowId.from_dict(d.pop("workflowId"))

        rule_update_errors = ComponentsschemasWorkflowTransitionRulesUpdateErrorDetailsRuleUpdateErrors.from_dict(
            d.pop("ruleUpdateErrors")
        )

        update_errors = cast(List[str], d.pop("updateErrors"))

        workflow_transition_rules_update_error_details = cls(
            workflow_id=workflow_id,
            rule_update_errors=rule_update_errors,
            update_errors=update_errors,
        )

        return workflow_transition_rules_update_error_details
