from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActorsMap")


@attr.s(auto_attribs=True)
class ActorsMap:
    """  """

    user: Union[Unset, List[str]] = UNSET
    group: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, List[str]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user

        group: Union[Unset, List[str]] = UNSET
        if not isinstance(self.group, Unset):
            group = self.group

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user = cast(List[str], d.pop("user", UNSET))

        group = cast(List[str], d.pop("group", UNSET))

        actors_map = cls(
            user=user,
            group=group,
        )

        return actors_map
