from enum import Enum


class GetWorkflowTransitionRuleConfigurationsTypesItem(str, Enum):
    POSTFUNCTION = "postfunction"
    CONDITION = "condition"
    VALIDATOR = "validator"

    def __str__(self) -> str:
        return str(self.value)
