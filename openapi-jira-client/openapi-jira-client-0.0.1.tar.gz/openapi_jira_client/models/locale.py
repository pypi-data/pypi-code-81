from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Locale")


@attr.s(auto_attribs=True)
class Locale:
    """ Details of a locale. """

    locale: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        locale = self.locale

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if locale is not UNSET:
            field_dict["locale"] = locale

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        locale = d.pop("locale", UNSET)

        locale = cls(
            locale=locale,
        )

        return locale
