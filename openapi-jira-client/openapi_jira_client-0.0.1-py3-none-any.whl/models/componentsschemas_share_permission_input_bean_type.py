from enum import Enum


class ComponentsschemasSharePermissionInputBeanType(str, Enum):
    PROJECT = "project"
    GROUP = "group"
    PROJECTROLE = "projectRole"
    GLOBAL_ = "global"
    AUTHENTICATED = "authenticated"

    def __str__(self) -> str:
        return str(self.value)
