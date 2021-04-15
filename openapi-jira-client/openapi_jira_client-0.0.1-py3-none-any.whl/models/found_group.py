from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.group_label import GroupLabel
from ..types import UNSET, Unset

T = TypeVar("T", bound="FoundGroup")


@attr.s(auto_attribs=True)
class FoundGroup:
    """ A group found in a search. """

    name: Union[Unset, str] = UNSET
    html: Union[Unset, str] = UNSET
    labels: Union[Unset, List[GroupLabel]] = UNSET
    group_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        html = self.html
        labels: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = []
            for labels_item_data in self.labels:
                labels_item = labels_item_data.to_dict()

                labels.append(labels_item)

        group_id = self.group_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if html is not UNSET:
            field_dict["html"] = html
        if labels is not UNSET:
            field_dict["labels"] = labels
        if group_id is not UNSET:
            field_dict["groupId"] = group_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        html = d.pop("html", UNSET)

        labels = []
        _labels = d.pop("labels", UNSET)
        for labels_item_data in _labels or []:
            labels_item = GroupLabel.from_dict(labels_item_data)

            labels.append(labels_item)

        group_id = d.pop("groupId", UNSET)

        found_group = cls(
            name=name,
            html=html,
            labels=labels,
            group_id=group_id,
        )

        return found_group
