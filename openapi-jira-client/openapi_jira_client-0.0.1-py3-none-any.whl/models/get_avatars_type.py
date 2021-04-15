from enum import Enum


class GetAvatarsType(str, Enum):
    PROJECT = "project"
    ISSUETYPE = "issuetype"

    def __str__(self) -> str:
        return str(self.value)
