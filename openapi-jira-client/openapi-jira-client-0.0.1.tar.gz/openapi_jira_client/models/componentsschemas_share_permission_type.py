from enum import Enum


class ComponentsschemasSharePermissionType(str, Enum):
    GROUP = "group"
    PROJECT = "project"
    PROJECTROLE = "projectRole"
    GLOBAL_ = "global"
    LOGGEDIN = "loggedin"
    AUTHENTICATED = "authenticated"
    PROJECT_UNKNOWN = "project-unknown"

    def __str__(self) -> str:
        return str(self.value)
