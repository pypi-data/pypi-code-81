from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlatesArchivalChange")


@attr.s(auto_attribs=True)
class PlatesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of plates along with any IDs of containers that were archived / unarchived."""

    container_ids: Union[Unset, List[str]] = UNSET
    plate_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        container_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.container_ids, Unset):
            container_ids = self.container_ids

        plate_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.plate_ids, Unset):
            plate_ids = self.plate_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if container_ids is not UNSET:
            field_dict["containerIds"] = container_ids
        if plate_ids is not UNSET:
            field_dict["plateIds"] = plate_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        container_ids = cast(List[str], d.pop("containerIds", UNSET))

        plate_ids = cast(List[str], d.pop("plateIds", UNSET))

        plates_archival_change = cls(
            container_ids=container_ids,
            plate_ids=plate_ids,
        )

        return plates_archival_change
