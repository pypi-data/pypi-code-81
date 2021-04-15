from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.group_name import GroupName
from ..models.user_details import UserDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationRecipients")


@attr.s(auto_attribs=True)
class NotificationRecipients:
    """ Details of the users and groups to receive the notification. """

    reporter: Union[Unset, bool] = UNSET
    assignee: Union[Unset, bool] = UNSET
    watchers: Union[Unset, bool] = UNSET
    voters: Union[Unset, bool] = UNSET
    users: Union[Unset, List[UserDetails]] = UNSET
    groups: Union[Unset, List[GroupName]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reporter = self.reporter
        assignee = self.assignee
        watchers = self.watchers
        voters = self.voters
        users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()

                users.append(users_item)

        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reporter is not UNSET:
            field_dict["reporter"] = reporter
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if watchers is not UNSET:
            field_dict["watchers"] = watchers
        if voters is not UNSET:
            field_dict["voters"] = voters
        if users is not UNSET:
            field_dict["users"] = users
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reporter = d.pop("reporter", UNSET)

        assignee = d.pop("assignee", UNSET)

        watchers = d.pop("watchers", UNSET)

        voters = d.pop("voters", UNSET)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = UserDetails.from_dict(users_item_data)

            users.append(users_item)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = GroupName.from_dict(groups_item_data)

            groups.append(groups_item)

        notification_recipients = cls(
            reporter=reporter,
            assignee=assignee,
            watchers=watchers,
            voters=voters,
            users=users,
            groups=groups,
        )

        notification_recipients.additional_properties = d
        return notification_recipients

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
