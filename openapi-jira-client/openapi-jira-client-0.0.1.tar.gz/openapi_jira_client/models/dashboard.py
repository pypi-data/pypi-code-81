from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.share_permission import SharePermission
from ..models.user_bean import UserBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="Dashboard")


@attr.s(auto_attribs=True)
class Dashboard:
    """ Details of a dashboard. """

    description: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    is_favourite: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, UserBean] = UNSET
    popularity: Union[Unset, int] = UNSET
    rank: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    share_permissions: Union[Unset, List[SharePermission]] = UNSET
    view: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        id_ = self.id_
        is_favourite = self.is_favourite
        name = self.name
        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        popularity = self.popularity
        rank = self.rank
        self_ = self.self_
        share_permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.share_permissions, Unset):
            share_permissions = []
            for share_permissions_item_data in self.share_permissions:
                share_permissions_item = share_permissions_item_data.to_dict()

                share_permissions.append(share_permissions_item)

        view = self.view

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if id_ is not UNSET:
            field_dict["id"] = id_
        if is_favourite is not UNSET:
            field_dict["isFavourite"] = is_favourite
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner
        if popularity is not UNSET:
            field_dict["popularity"] = popularity
        if rank is not UNSET:
            field_dict["rank"] = rank
        if self_ is not UNSET:
            field_dict["self"] = self_
        if share_permissions is not UNSET:
            field_dict["sharePermissions"] = share_permissions
        if view is not UNSET:
            field_dict["view"] = view

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        id_ = d.pop("id", UNSET)

        is_favourite = d.pop("isFavourite", UNSET)

        name = d.pop("name", UNSET)

        owner: Union[Unset, UserBean] = UNSET
        _owner = d.pop("owner", UNSET)
        if not isinstance(_owner, Unset):
            owner = UserBean.from_dict(_owner)

        popularity = d.pop("popularity", UNSET)

        rank = d.pop("rank", UNSET)

        self_ = d.pop("self", UNSET)

        share_permissions = []
        _share_permissions = d.pop("sharePermissions", UNSET)
        for share_permissions_item_data in _share_permissions or []:
            share_permissions_item = SharePermission.from_dict(share_permissions_item_data)

            share_permissions.append(share_permissions_item)

        view = d.pop("view", UNSET)

        dashboard = cls(
            description=description,
            id_=id_,
            is_favourite=is_favourite,
            name=name,
            owner=owner,
            popularity=popularity,
            rank=rank,
            self_=self_,
            share_permissions=share_permissions,
            view=view,
        )

        return dashboard
