from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AvatarUrlsBean")


@attr.s(auto_attribs=True)
class AvatarUrlsBean:
    """  """

    field_16x16: Union[Unset, str] = UNSET
    field_24x24: Union[Unset, str] = UNSET
    field_32x32: Union[Unset, str] = UNSET
    field_48x48: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field_16x16 = self.field_16x16
        field_24x24 = self.field_24x24
        field_32x32 = self.field_32x32
        field_48x48 = self.field_48x48

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if field_16x16 is not UNSET:
            field_dict["16x16"] = field_16x16
        if field_24x24 is not UNSET:
            field_dict["24x24"] = field_24x24
        if field_32x32 is not UNSET:
            field_dict["32x32"] = field_32x32
        if field_48x48 is not UNSET:
            field_dict["48x48"] = field_48x48

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_16x16 = d.pop("16x16", UNSET)

        field_24x24 = d.pop("24x24", UNSET)

        field_32x32 = d.pop("32x32", UNSET)

        field_48x48 = d.pop("48x48", UNSET)

        avatar_urls_bean = cls(
            field_16x16=field_16x16,
            field_24x24=field_24x24,
            field_32x32=field_32x32,
            field_48x48=field_48x48,
        )

        return avatar_urls_bean
