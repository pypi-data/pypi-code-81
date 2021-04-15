from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.field_last_used import FieldLastUsed
from ..models.json_type_bean import JsonTypeBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="Field")


@attr.s(auto_attribs=True)
class Field:
    """ Details of a field. """

    id_: str
    name: str
    schema: JsonTypeBean
    description: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    is_locked: Union[Unset, bool] = UNSET
    searcher_key: Union[Unset, str] = UNSET
    screens_count: Union[Unset, int] = UNSET
    contexts_count: Union[Unset, int] = UNSET
    last_used: Union[Unset, FieldLastUsed] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        schema = self.schema.to_dict()

        description = self.description
        key = self.key
        is_locked = self.is_locked
        searcher_key = self.searcher_key
        screens_count = self.screens_count
        contexts_count = self.contexts_count
        last_used: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_used, Unset):
            last_used = self.last_used.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
                "schema": schema,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if key is not UNSET:
            field_dict["key"] = key
        if is_locked is not UNSET:
            field_dict["isLocked"] = is_locked
        if searcher_key is not UNSET:
            field_dict["searcherKey"] = searcher_key
        if screens_count is not UNSET:
            field_dict["screensCount"] = screens_count
        if contexts_count is not UNSET:
            field_dict["contextsCount"] = contexts_count
        if last_used is not UNSET:
            field_dict["lastUsed"] = last_used

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        schema = JsonTypeBean.from_dict(d.pop("schema"))

        description = d.pop("description", UNSET)

        key = d.pop("key", UNSET)

        is_locked = d.pop("isLocked", UNSET)

        searcher_key = d.pop("searcherKey", UNSET)

        screens_count = d.pop("screensCount", UNSET)

        contexts_count = d.pop("contextsCount", UNSET)

        last_used: Union[Unset, FieldLastUsed] = UNSET
        _last_used = d.pop("lastUsed", UNSET)
        if not isinstance(_last_used, Unset):
            last_used = FieldLastUsed.from_dict(_last_used)

        field = cls(
            id_=id_,
            name=name,
            schema=schema,
            description=description,
            key=key,
            is_locked=is_locked,
            searcher_key=searcher_key,
            screens_count=screens_count,
            contexts_count=contexts_count,
            last_used=last_used,
        )

        return field
