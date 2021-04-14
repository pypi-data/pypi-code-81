from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.container_quantity_units import ContainerQuantityUnits
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerQuantity")


@attr.s(auto_attribs=True)
class ContainerQuantity:
    """ Quantity of a container, well, or transfer. Supports solid and liquid quantities. """

    units: Union[Unset, None, ContainerQuantityUnits] = UNSET
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
            units = ContainerQuantityUnits(_units)

        value = d.pop("value", UNSET)

        container_quantity = cls(
            units=units,
            value=value,
        )

        return container_quantity
