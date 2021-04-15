from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.filter_subscription import FilterSubscription
from ..models.share_permission import SharePermission
from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterDetails")


@attr.s(auto_attribs=True)
class FilterDetails:
    """ Details of a filter. """

    name: str
    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    owner: Union[Unset, User] = UNSET
    jql: Union[Unset, str] = UNSET
    view_url: Union[Unset, str] = UNSET
    search_url: Union[Unset, str] = UNSET
    favourite: Union[Unset, bool] = UNSET
    favourited_count: Union[Unset, int] = UNSET
    share_permissions: Union[Unset, List[SharePermission]] = UNSET
    subscriptions: Union[Unset, List[FilterSubscription]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        self_ = self.self_
        id_ = self.id_
        description = self.description
        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        jql = self.jql
        view_url = self.view_url
        search_url = self.search_url
        favourite = self.favourite
        favourited_count = self.favourited_count
        share_permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.share_permissions, Unset):
            share_permissions = []
            for share_permissions_item_data in self.share_permissions:
                share_permissions_item = share_permissions_item_data.to_dict()

                share_permissions.append(share_permissions_item)

        subscriptions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subscriptions, Unset):
            subscriptions = []
            for subscriptions_item_data in self.subscriptions:
                subscriptions_item = subscriptions_item_data.to_dict()

                subscriptions.append(subscriptions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if description is not UNSET:
            field_dict["description"] = description
        if owner is not UNSET:
            field_dict["owner"] = owner
        if jql is not UNSET:
            field_dict["jql"] = jql
        if view_url is not UNSET:
            field_dict["viewUrl"] = view_url
        if search_url is not UNSET:
            field_dict["searchUrl"] = search_url
        if favourite is not UNSET:
            field_dict["favourite"] = favourite
        if favourited_count is not UNSET:
            field_dict["favouritedCount"] = favourited_count
        if share_permissions is not UNSET:
            field_dict["sharePermissions"] = share_permissions
        if subscriptions is not UNSET:
            field_dict["subscriptions"] = subscriptions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        owner: Union[Unset, User] = UNSET
        _owner = d.pop("owner", UNSET)
        if not isinstance(_owner, Unset):
            owner = User.from_dict(_owner)

        jql = d.pop("jql", UNSET)

        view_url = d.pop("viewUrl", UNSET)

        search_url = d.pop("searchUrl", UNSET)

        favourite = d.pop("favourite", UNSET)

        favourited_count = d.pop("favouritedCount", UNSET)

        share_permissions = []
        _share_permissions = d.pop("sharePermissions", UNSET)
        for share_permissions_item_data in _share_permissions or []:
            share_permissions_item = SharePermission.from_dict(share_permissions_item_data)

            share_permissions.append(share_permissions_item)

        subscriptions = []
        _subscriptions = d.pop("subscriptions", UNSET)
        for subscriptions_item_data in _subscriptions or []:
            subscriptions_item = FilterSubscription.from_dict(subscriptions_item_data)

            subscriptions.append(subscriptions_item)

        filter_details = cls(
            name=name,
            self_=self_,
            id_=id_,
            description=description,
            owner=owner,
            jql=jql,
            view_url=view_url,
            search_url=search_url,
            favourite=favourite,
            favourited_count=favourited_count,
            share_permissions=share_permissions,
            subscriptions=subscriptions,
        )

        return filter_details
