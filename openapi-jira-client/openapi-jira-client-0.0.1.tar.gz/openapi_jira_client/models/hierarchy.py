from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.hierarchy_level import HierarchyLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="Hierarchy")


@attr.s(auto_attribs=True)
class Hierarchy:
    """ The project issue type hierarchy. """

    base_level_id: Union[Unset, int] = UNSET
    levels: Union[Unset, List[HierarchyLevel]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        base_level_id = self.base_level_id
        levels: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.levels, Unset):
            levels = []
            for levels_item_data in self.levels:
                levels_item = levels_item_data.to_dict()

                levels.append(levels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if base_level_id is not UNSET:
            field_dict["baseLevelId"] = base_level_id
        if levels is not UNSET:
            field_dict["levels"] = levels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_level_id = d.pop("baseLevelId", UNSET)

        levels = []
        _levels = d.pop("levels", UNSET)
        for levels_item_data in _levels or []:
            levels_item = HierarchyLevel.from_dict(levels_item_data)

            levels.append(levels_item)

        hierarchy = cls(
            base_level_id=base_level_id,
            levels=levels,
        )

        return hierarchy
