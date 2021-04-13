from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTask")


@attr.s(auto_attribs=True)
class RequestTask:
    """A request task."""

    id: str
    schema: Union[Unset, None, SchemaSummary] = UNSET
    fields: Union[Unset, Fields] = UNSET
    sample_group_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        sample_group_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.sample_group_ids, Unset):
            sample_group_ids = self.sample_group_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if schema is not UNSET:
            field_dict["schema"] = schema
        if fields is not UNSET:
            field_dict["fields"] = fields
        if sample_group_ids is not UNSET:
            field_dict["sampleGroupIds"] = sample_group_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(_schema)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds", UNSET))

        request_task = cls(
            id=id,
            schema=schema,
            fields=fields,
            sample_group_ids=sample_group_ids,
        )

        return request_task
