from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateScreenTypes")


@attr.s(auto_attribs=True)
class UpdateScreenTypes:
    """ The IDs of the screens for the screen types of the screen scheme. """

    edit: Union[Unset, str] = UNSET
    create: Union[Unset, str] = UNSET
    view: Union[Unset, str] = UNSET
    default: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        edit = self.edit
        create = self.create
        view = self.view
        default = self.default

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if edit is not UNSET:
            field_dict["edit"] = edit
        if create is not UNSET:
            field_dict["create"] = create
        if view is not UNSET:
            field_dict["view"] = view
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        edit = d.pop("edit", UNSET)

        create = d.pop("create", UNSET)

        view = d.pop("view", UNSET)

        default = d.pop("default", UNSET)

        update_screen_types = cls(
            edit=edit,
            create=create,
            view=view,
            default=default,
        )

        return update_screen_types
