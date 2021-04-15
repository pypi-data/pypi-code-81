from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.page_bean_issue_type_screen_scheme import PageBeanIssueTypeScreenScheme
from ..models.screen_types import ScreenTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScreenScheme")


@attr.s(auto_attribs=True)
class ScreenScheme:
    """ A screen scheme. """

    id_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    screens: Union[Unset, ScreenTypes] = UNSET
    issue_type_screen_schemes: Union[Unset, PageBeanIssueTypeScreenScheme] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        screens: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.screens, Unset):
            screens = self.screens.to_dict()

        issue_type_screen_schemes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issue_type_screen_schemes, Unset):
            issue_type_screen_schemes = self.issue_type_screen_schemes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if screens is not UNSET:
            field_dict["screens"] = screens
        if issue_type_screen_schemes is not UNSET:
            field_dict["issueTypeScreenSchemes"] = issue_type_screen_schemes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        screens: Union[Unset, ScreenTypes] = UNSET
        _screens = d.pop("screens", UNSET)
        if not isinstance(_screens, Unset):
            screens = ScreenTypes.from_dict(_screens)

        issue_type_screen_schemes: Union[Unset, PageBeanIssueTypeScreenScheme] = UNSET
        _issue_type_screen_schemes = d.pop("issueTypeScreenSchemes", UNSET)
        if not isinstance(_issue_type_screen_schemes, Unset):
            issue_type_screen_schemes = PageBeanIssueTypeScreenScheme.from_dict(_issue_type_screen_schemes)

        screen_scheme = cls(
            id_=id_,
            name=name,
            description=description,
            screens=screens,
            issue_type_screen_schemes=issue_type_screen_schemes,
        )

        return screen_scheme
