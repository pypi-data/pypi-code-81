import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.change_details import ChangeDetails
from ..models.history_metadata import HistoryMetadata
from ..models.user_details import UserDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Changelog")


@attr.s(auto_attribs=True)
class Changelog:
    """ A changelog. """

    id_: Union[Unset, str] = UNSET
    author: Union[Unset, UserDetails] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    items: Union[Unset, List[ChangeDetails]] = UNSET
    history_metadata: Union[Unset, HistoryMetadata] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        author: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()

                items.append(items_item)

        history_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.history_metadata, Unset):
            history_metadata = self.history_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if author is not UNSET:
            field_dict["author"] = author
        if created is not UNSET:
            field_dict["created"] = created
        if items is not UNSET:
            field_dict["items"] = items
        if history_metadata is not UNSET:
            field_dict["historyMetadata"] = history_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        author: Union[Unset, UserDetails] = UNSET
        _author = d.pop("author", UNSET)
        if not isinstance(_author, Unset):
            author = UserDetails.from_dict(_author)

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = ChangeDetails.from_dict(items_item_data)

            items.append(items_item)

        history_metadata: Union[Unset, HistoryMetadata] = UNSET
        _history_metadata = d.pop("historyMetadata", UNSET)
        if not isinstance(_history_metadata, Unset):
            history_metadata = HistoryMetadata.from_dict(_history_metadata)

        changelog = cls(
            id_=id_,
            author=author,
            created=created,
            items=items,
            history_metadata=history_metadata,
        )

        return changelog
