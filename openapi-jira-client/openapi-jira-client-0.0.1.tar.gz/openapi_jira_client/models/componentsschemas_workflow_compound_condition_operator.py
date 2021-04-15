from enum import Enum


class ComponentsschemasWorkflowCompoundConditionOperator(str, Enum):
    AND_ = "AND"
    OR_ = "OR"

    def __str__(self) -> str:
        return str(self.value)
