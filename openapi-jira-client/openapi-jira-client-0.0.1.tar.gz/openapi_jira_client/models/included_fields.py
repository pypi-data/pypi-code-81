from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IncludedFields")


@attr.s(auto_attribs=True)
class IncludedFields:
    """  """

    excluded: Union[Unset, List[str]] = UNSET
    included: Union[Unset, List[str]] = UNSET
    actually_included: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        excluded: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded, Unset):
            excluded = self.excluded

        included: Union[Unset, List[str]] = UNSET
        if not isinstance(self.included, Unset):
            included = self.included

        actually_included: Union[Unset, List[str]] = UNSET
        if not isinstance(self.actually_included, Unset):
            actually_included = self.actually_included

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if excluded is not UNSET:
            field_dict["excluded"] = excluded
        if included is not UNSET:
            field_dict["included"] = included
        if actually_included is not UNSET:
            field_dict["actuallyIncluded"] = actually_included

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        excluded = cast(List[str], d.pop("excluded", UNSET))

        included = cast(List[str], d.pop("included", UNSET))

        actually_included = cast(List[str], d.pop("actuallyIncluded", UNSET))

        included_fields = cls(
            excluded=excluded,
            included=included,
            actually_included=actually_included,
        )

        return included_fields
