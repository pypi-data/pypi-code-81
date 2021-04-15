from enum import Enum


class SearchProjectsStatusItem(str, Enum):
    LIVE = "live"
    ARCHIVED = "archived"
    DELETED = "deleted"

    def __str__(self) -> str:
        return str(self.value)
