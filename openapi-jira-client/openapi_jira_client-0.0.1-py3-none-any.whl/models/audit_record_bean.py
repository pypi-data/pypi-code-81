import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.associated_item_bean import AssociatedItemBean
from ..models.changed_value_bean import ChangedValueBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditRecordBean")


@attr.s(auto_attribs=True)
class AuditRecordBean:
    """ An audit record. """

    id_: Union[Unset, int] = UNSET
    summary: Union[Unset, str] = UNSET
    remote_address: Union[Unset, str] = UNSET
    author_key: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    category: Union[Unset, str] = UNSET
    event_source: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    object_item: Union[Unset, AssociatedItemBean] = UNSET
    changed_values: Union[Unset, List[ChangedValueBean]] = UNSET
    associated_items: Union[Unset, List[AssociatedItemBean]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        summary = self.summary
        remote_address = self.remote_address
        author_key = self.author_key
        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        category = self.category
        event_source = self.event_source
        description = self.description
        object_item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.object_item, Unset):
            object_item = self.object_item.to_dict()

        changed_values: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.changed_values, Unset):
            changed_values = []
            for changed_values_item_data in self.changed_values:
                changed_values_item = changed_values_item_data.to_dict()

                changed_values.append(changed_values_item)

        associated_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.associated_items, Unset):
            associated_items = []
            for associated_items_item_data in self.associated_items:
                associated_items_item = associated_items_item_data.to_dict()

                associated_items.append(associated_items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if summary is not UNSET:
            field_dict["summary"] = summary
        if remote_address is not UNSET:
            field_dict["remoteAddress"] = remote_address
        if author_key is not UNSET:
            field_dict["authorKey"] = author_key
        if created is not UNSET:
            field_dict["created"] = created
        if category is not UNSET:
            field_dict["category"] = category
        if event_source is not UNSET:
            field_dict["eventSource"] = event_source
        if description is not UNSET:
            field_dict["description"] = description
        if object_item is not UNSET:
            field_dict["objectItem"] = object_item
        if changed_values is not UNSET:
            field_dict["changedValues"] = changed_values
        if associated_items is not UNSET:
            field_dict["associatedItems"] = associated_items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        summary = d.pop("summary", UNSET)

        remote_address = d.pop("remoteAddress", UNSET)

        author_key = d.pop("authorKey", UNSET)

        created: Union[Unset, datetime.datetime] = UNSET
        _created = d.pop("created", UNSET)
        if not isinstance(_created, Unset):
            created = isoparse(_created)

        category = d.pop("category", UNSET)

        event_source = d.pop("eventSource", UNSET)

        description = d.pop("description", UNSET)

        object_item: Union[Unset, AssociatedItemBean] = UNSET
        _object_item = d.pop("objectItem", UNSET)
        if not isinstance(_object_item, Unset):
            object_item = AssociatedItemBean.from_dict(_object_item)

        changed_values = []
        _changed_values = d.pop("changedValues", UNSET)
        for changed_values_item_data in _changed_values or []:
            changed_values_item = ChangedValueBean.from_dict(changed_values_item_data)

            changed_values.append(changed_values_item)

        associated_items = []
        _associated_items = d.pop("associatedItems", UNSET)
        for associated_items_item_data in _associated_items or []:
            associated_items_item = AssociatedItemBean.from_dict(associated_items_item_data)

            associated_items.append(associated_items_item)

        audit_record_bean = cls(
            id_=id_,
            summary=summary,
            remote_address=remote_address,
            author_key=author_key,
            created=created,
            category=category,
            event_source=event_source,
            description=description,
            object_item=object_item,
            changed_values=changed_values,
            associated_items=associated_items,
        )

        return audit_record_bean
