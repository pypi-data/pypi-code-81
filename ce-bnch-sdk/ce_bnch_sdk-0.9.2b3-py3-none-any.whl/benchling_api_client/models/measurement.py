from typing import Any, Dict, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="Measurement")


@attr.s(auto_attribs=True)
class Measurement:
    """  """

    units: Optional[str]
    value: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        units = self.units
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "units": units,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = d.pop("units")

        value = d.pop("value")

        measurement = cls(
            units=units,
            value=value,
        )

        return measurement
