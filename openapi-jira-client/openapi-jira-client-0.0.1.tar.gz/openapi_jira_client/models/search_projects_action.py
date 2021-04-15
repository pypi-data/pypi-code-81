from enum import Enum


class SearchProjectsAction(str, Enum):
    VIEW = "view"
    BROWSE = "browse"
    EDIT = "edit"

    def __str__(self) -> str:
        return str(self.value)
