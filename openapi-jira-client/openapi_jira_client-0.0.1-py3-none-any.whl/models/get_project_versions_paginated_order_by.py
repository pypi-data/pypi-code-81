from enum import Enum


class GetProjectVersionsPaginatedOrderBy(str, Enum):
    DESCRIPTION = "description"
    VALUE_1 = "-description"
    VALUE_2 = "+description"
    NAME = "name"
    VALUE_4 = "-name"
    VALUE_5 = "+name"
    RELEASEDATE = "releaseDate"
    VALUE_7 = "-releaseDate"
    VALUE_8 = "+releaseDate"
    SEQUENCE = "sequence"
    VALUE_10 = "-sequence"
    VALUE_11 = "+sequence"
    STARTDATE = "startDate"
    VALUE_13 = "-startDate"
    VALUE_14 = "+startDate"

    def __str__(self) -> str:
        return str(self.value)
