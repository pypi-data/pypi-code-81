from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.container_volume_units import ContainerVolumeUnits
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerVolume")


@attr.s(auto_attribs=True)
class ContainerVolume:
    """ Volume of a container, well, or transfer. Only supports liquid quantities. """

    units: Union[Unset, None, ContainerVolumeUnits] = UNSET
    value: Union[Unset, None, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        units: Union[Unset, None, int] = UNSET
        if not isinstance(self.units, Unset):
            units = self.units.value if self.units else None

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = None
        _units = d.pop("units", UNSET)
        if _units is not None and _units is not UNSET:
            units = ContainerVolumeUnits(_units)

        value = d.pop("value", UNSET)

        container_volume = cls(
            units=units,
            value=value,
        )

        return container_volume
