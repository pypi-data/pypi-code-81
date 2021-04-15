from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationRole")


@attr.s(auto_attribs=True)
class ApplicationRole:
    """ Details of an application role. """

    key: Union[Unset, str] = UNSET
    groups: Union[Unset, List[str]] = UNSET
    name: Union[Unset, str] = UNSET
    default_groups: Union[Unset, List[str]] = UNSET
    selected_by_default: Union[Unset, bool] = UNSET
    defined: Union[Unset, bool] = UNSET
    number_of_seats: Union[Unset, int] = UNSET
    remaining_seats: Union[Unset, int] = UNSET
    user_count: Union[Unset, int] = UNSET
    user_count_description: Union[Unset, str] = UNSET
    has_unlimited_seats: Union[Unset, bool] = UNSET
    platform: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        name = self.name
        default_groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.default_groups, Unset):
            default_groups = self.default_groups

        selected_by_default = self.selected_by_default
        defined = self.defined
        number_of_seats = self.number_of_seats
        remaining_seats = self.remaining_seats
        user_count = self.user_count
        user_count_description = self.user_count_description
        has_unlimited_seats = self.has_unlimited_seats
        platform = self.platform

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if groups is not UNSET:
            field_dict["groups"] = groups
        if name is not UNSET:
            field_dict["name"] = name
        if default_groups is not UNSET:
            field_dict["defaultGroups"] = default_groups
        if selected_by_default is not UNSET:
            field_dict["selectedByDefault"] = selected_by_default
        if defined is not UNSET:
            field_dict["defined"] = defined
        if number_of_seats is not UNSET:
            field_dict["numberOfSeats"] = number_of_seats
        if remaining_seats is not UNSET:
            field_dict["remainingSeats"] = remaining_seats
        if user_count is not UNSET:
            field_dict["userCount"] = user_count
        if user_count_description is not UNSET:
            field_dict["userCountDescription"] = user_count_description
        if has_unlimited_seats is not UNSET:
            field_dict["hasUnlimitedSeats"] = has_unlimited_seats
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        groups = cast(List[str], d.pop("groups", UNSET))

        name = d.pop("name", UNSET)

        default_groups = cast(List[str], d.pop("defaultGroups", UNSET))

        selected_by_default = d.pop("selectedByDefault", UNSET)

        defined = d.pop("defined", UNSET)

        number_of_seats = d.pop("numberOfSeats", UNSET)

        remaining_seats = d.pop("remainingSeats", UNSET)

        user_count = d.pop("userCount", UNSET)

        user_count_description = d.pop("userCountDescription", UNSET)

        has_unlimited_seats = d.pop("hasUnlimitedSeats", UNSET)

        platform = d.pop("platform", UNSET)

        application_role = cls(
            key=key,
            groups=groups,
            name=name,
            default_groups=default_groups,
            selected_by_default=selected_by_default,
            defined=defined,
            number_of_seats=number_of_seats,
            remaining_seats=remaining_seats,
            user_count=user_count,
            user_count_description=user_count_description,
            has_unlimited_seats=has_unlimited_seats,
            platform=platform,
        )

        return application_role
