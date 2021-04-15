from enum import Enum


class ComponentsschemasEventNotificationNotificationType(str, Enum):
    CURRENTASSIGNEE = "CurrentAssignee"
    REPORTER = "Reporter"
    CURRENTUSER = "CurrentUser"
    PROJECTLEAD = "ProjectLead"
    COMPONENTLEAD = "ComponentLead"
    USER = "User"
    GROUP = "Group"
    PROJECTROLE = "ProjectRole"
    EMAILADDRESS = "EmailAddress"
    ALLWATCHERS = "AllWatchers"
    USERCUSTOMFIELD = "UserCustomField"
    GROUPCUSTOMFIELD = "GroupCustomField"

    def __str__(self) -> str:
        return str(self.value)
