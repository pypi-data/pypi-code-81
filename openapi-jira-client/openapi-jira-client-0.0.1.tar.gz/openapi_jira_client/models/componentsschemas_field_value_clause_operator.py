from enum import Enum


class ComponentsschemasFieldValueClauseOperator(str, Enum):
    VALUE_0 = "="
    VALUE_1 = "!="
    VALUE_2 = ">"
    VALUE_3 = "<"
    VALUE_4 = ">="
    VALUE_5 = "<="
    IN_ = "in"
    NOT_IN = "not in"
    VALUE_8 = "~"
    VALUE_9 = "~="
    IS_ = "is"
    IS_NOT = "is not"

    def __str__(self) -> str:
        return str(self.value)
