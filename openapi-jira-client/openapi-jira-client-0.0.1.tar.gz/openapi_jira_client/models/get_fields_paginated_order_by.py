from enum import Enum


class GetFieldsPaginatedOrderBy(str, Enum):
    CONTEXTSCOUNT = "contextsCount"
    VALUE_1 = "-contextsCount"
    VALUE_2 = "+contextsCount"
    LASTUSED = "lastUsed"
    VALUE_4 = "-lastUsed"
    VALUE_5 = "+lastUsed"
    NAME = "name"
    VALUE_7 = "-name"
    VALUE_8 = "+name"
    SCREENSCOUNT = "screensCount"
    VALUE_10 = "-screensCount"
    VALUE_11 = "+screensCount"

    def __str__(self) -> str:
        return str(self.value)
