from enum import Enum


class GetProjectComponentsPaginatedOrderBy(str, Enum):
    DESCRIPTION = "description"
    VALUE_1 = "-description"
    VALUE_2 = "+description"
    ISSUECOUNT = "issueCount"
    VALUE_4 = "-issueCount"
    VALUE_5 = "+issueCount"
    LEAD = "lead"
    VALUE_7 = "-lead"
    VALUE_8 = "+lead"
    NAME = "name"
    VALUE_10 = "-name"
    VALUE_11 = "+name"

    def __str__(self) -> str:
        return str(self.value)
