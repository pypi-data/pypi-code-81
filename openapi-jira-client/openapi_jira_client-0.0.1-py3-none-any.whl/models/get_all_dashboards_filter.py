from enum import Enum


class GetAllDashboardsFilter(str, Enum):
    MY = "my"
    FAVOURITE = "favourite"

    def __str__(self) -> str:
        return str(self.value)
