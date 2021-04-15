import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.entity_property import EntityProperty
from ..models.user_details import UserDetails
from ..models.visibility import Visibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="Worklog")


@attr.s(auto_attribs=True)
class Worklog:
    """ Details of a worklog. """

    self_: Union[Unset, str] = UNSET
    author: Union[Unset, UserDetails] = UNSET
    update_author: Union[Unset, UserDetails] = UNSET
    comment: Union[Unset, None] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    visibility: Union[Unset, Visibility] = UNSET
    started: Union[Unset, datetime.datetime] = UNSET
    time_spent: Union[Unset, str] = UNSET
    time_spent_seconds: Union[Unset, int] = UNSET
    id_: Union[Unset, str] = UNSET
    issue_id: Union[Unset, str] = UNSET
    properties: Union[Unset, List[EntityProperty]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        author: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        update_author: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.update_author, Unset):
            update_author = self.update_author.to_dict()

        comment = None

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        visibility: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.to_dict()

        started: Union[Unset, str] = UNSET
        if not isinstance(self.started, Unset):
            started = self.started.isoformat()

        time_spent = self.time_spent
        time_spent_seconds = self.time_spent_seconds
        id_ = self.id_
        issue_id = self.issue_id
        properties: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for properties_item_data in self.properties:
                properties_item = properties_item_data.to_dict()

                properties.append(properties_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if author is not UNSET:
            field_dict["author"] = author
        if update_author is not UNSET:
            field_dict["updateAuthor"] = update_author
        if comment is not UNSET:
            field_dict["comment"] = comment
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if started is not UNSET:
            field_dict["started"] = started
        if time_spent is not UNSET:
            field_dict["timeSpent"] = time_spent
        if time_spent_seconds is not UNSET:
            field_dict["timeSpentSeconds"] = time_spent_seconds
        if id_ is not UNSET:
            field_dict["id"] = id_
        if issue_id is not UNSET:
            field_dict["issueId"] = issue_id
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        author: Union[Unset, UserDetails] = UNSET
        _author = d.pop("author", UNSET)
        if not isinstance(_author, Unset):
            author = UserDetails.from_dict(_author)

        update_author: Union[Unset, UserDetails] = UNSET
        _update_author = d.pop("updateAuthor", UNSET)
        if not isinstance(_update_author, Unset):
            update_author = UserDetails.from_dict(_update_author)

        comment = None

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        updated: Union[Unset, datetime.datetime] = UNSET
        _updated = d.pop("updated", UNSET)
        if not isinstance(_updated, Unset):
            updated = isoparse(_updated)

        visibility: Union[Unset, Visibility] = UNSET
        _visibility = d.pop("visibility", UNSET)
        if not isinstance(_visibility, Unset):
            visibility = Visibility.from_dict(_visibility)

        started: Union[Unset, datetime.datetime] = UNSET
        _started = d.pop("started", UNSET)
        if not isinstance(_started, Unset):
            started = isoparse(_started)

        time_spent = d.pop("timeSpent", UNSET)

        time_spent_seconds = d.pop("timeSpentSeconds", UNSET)

        id_ = d.pop("id", UNSET)

        issue_id = d.pop("issueId", UNSET)

        properties = []
        _properties = d.pop("properties", UNSET)
        for properties_item_data in _properties or []:
            properties_item = EntityProperty.from_dict(properties_item_data)

            properties.append(properties_item)

        worklog = cls(
            self_=self_,
            author=author,
            update_author=update_author,
            comment=comment,
            created=created,
            updated=updated,
            visibility=visibility,
            started=started,
            time_spent=time_spent,
            time_spent_seconds=time_spent_seconds,
            id_=id_,
            issue_id=issue_id,
            properties=properties,
        )

        worklog.additional_properties = d
        return worklog

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
