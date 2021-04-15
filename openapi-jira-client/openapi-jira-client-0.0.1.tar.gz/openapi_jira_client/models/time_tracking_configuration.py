from typing import Any, Dict, Type, TypeVar

import attr

from ..models.componentsschemas_time_tracking_configuration_default_unit import (
    ComponentsschemasTimeTrackingConfigurationDefaultUnit,
)
from ..models.componentsschemas_time_tracking_configuration_time_format import (
    ComponentsschemasTimeTrackingConfigurationTimeFormat,
)

T = TypeVar("T", bound="TimeTrackingConfiguration")


@attr.s(auto_attribs=True)
class TimeTrackingConfiguration:
    """ Details of the time tracking configuration. """

    working_hours_per_day: float
    working_days_per_week: float
    time_format: ComponentsschemasTimeTrackingConfigurationTimeFormat
    default_unit: ComponentsschemasTimeTrackingConfigurationDefaultUnit

    def to_dict(self) -> Dict[str, Any]:
        working_hours_per_day = self.working_hours_per_day
        working_days_per_week = self.working_days_per_week
        time_format = self.time_format.value

        default_unit = self.default_unit.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workingHoursPerDay": working_hours_per_day,
                "workingDaysPerWeek": working_days_per_week,
                "timeFormat": time_format,
                "defaultUnit": default_unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        working_hours_per_day = d.pop("workingHoursPerDay")

        working_days_per_week = d.pop("workingDaysPerWeek")

        time_format = ComponentsschemasTimeTrackingConfigurationTimeFormat(d.pop("timeFormat"))

        default_unit = ComponentsschemasTimeTrackingConfigurationDefaultUnit(d.pop("defaultUnit"))

        time_tracking_configuration = cls(
            working_hours_per_day=working_hours_per_day,
            working_days_per_week=working_days_per_week,
            time_format=time_format,
            default_unit=default_unit,
        )

        return time_tracking_configuration
