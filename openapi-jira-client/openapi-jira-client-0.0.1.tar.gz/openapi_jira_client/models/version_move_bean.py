from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_version_move_bean_position import ComponentsschemasVersionMoveBeanPosition
from ..types import UNSET, Unset

T = TypeVar("T", bound="VersionMoveBean")


@attr.s(auto_attribs=True)
class VersionMoveBean:
    """  """

    after: Union[Unset, str] = UNSET
    position: Union[Unset, ComponentsschemasVersionMoveBeanPosition] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        after = self.after
        position: Union[Unset, str] = UNSET
        if not isinstance(self.position, Unset):
            position = self.position.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if after is not UNSET:
            field_dict["after"] = after
        if position is not UNSET:
            field_dict["position"] = position

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        after = d.pop("after", UNSET)

        position: Union[Unset, ComponentsschemasVersionMoveBeanPosition] = UNSET
        _position = d.pop("position", UNSET)
        if not isinstance(_position, Unset):
            position = ComponentsschemasVersionMoveBeanPosition(_position)

        version_move_bean = cls(
            after=after,
            position=position,
        )

        return version_move_bean
