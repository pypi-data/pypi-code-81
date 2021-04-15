from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="UpdateDefaultScreenScheme")


@attr.s(auto_attribs=True)
class UpdateDefaultScreenScheme:
    """ The ID of a screen scheme. """

    screen_scheme_id: str

    def to_dict(self) -> Dict[str, Any]:
        screen_scheme_id = self.screen_scheme_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "screenSchemeId": screen_scheme_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        screen_scheme_id = d.pop("screenSchemeId")

        update_default_screen_scheme = cls(
            screen_scheme_id=screen_scheme_id,
        )

        return update_default_screen_scheme
