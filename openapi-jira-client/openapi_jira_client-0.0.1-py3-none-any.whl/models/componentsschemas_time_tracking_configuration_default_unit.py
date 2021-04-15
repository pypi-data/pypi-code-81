from enum import Enum


class ComponentsschemasTimeTrackingConfigurationDefaultUnit(str, Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"

    def __str__(self) -> str:
        return str(self.value)
