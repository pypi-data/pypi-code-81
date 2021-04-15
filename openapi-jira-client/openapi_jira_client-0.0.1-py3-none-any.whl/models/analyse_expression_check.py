from enum import Enum


class AnalyseExpressionCheck(str, Enum):
    SYNTAX = "syntax"
    TYPE = "type"
    COMPLEXITY = "complexity"

    def __str__(self) -> str:
        return str(self.value)
