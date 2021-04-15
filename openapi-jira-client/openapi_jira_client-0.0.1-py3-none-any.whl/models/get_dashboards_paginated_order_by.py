from enum import Enum


class GetDashboardsPaginatedOrderBy(str, Enum):
    DESCRIPTION = "description"
    VALUE_1 = "-description"
    VALUE_2 = "+description"
    FAVORITE_COUNT = "favorite_count"
    VALUE_4 = "-favorite_count"
    VALUE_5 = "+favorite_count"
    ID = "id"
    VALUE_7 = "-id"
    VALUE_8 = "+id"
    IS_FAVORITE = "is_favorite"
    VALUE_10 = "-is_favorite"
    VALUE_11 = "+is_favorite"
    NAME = "name"
    VALUE_13 = "-name"
    VALUE_14 = "+name"
    OWNER = "owner"
    VALUE_16 = "-owner"
    VALUE_17 = "+owner"

    def __str__(self) -> str:
        return str(self.value)
