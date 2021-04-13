from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryCreate")


@attr.s(auto_attribs=True)
class EntryCreate:
    """  """

    folder_id: str
    name: str
    author_ids: Union[Unset, str] = UNSET
    custom_fields: Union[Unset, CustomFields] = UNSET
    entry_template_id: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    schema_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        folder_id = self.folder_id
        name = self.name
        author_ids = self.author_ids
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        entry_template_id = self.entry_template_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "folderId": folder_id,
                "name": name,
            }
        )
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entry_template_id is not UNSET:
            field_dict["entryTemplateId"] = entry_template_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_id = d.pop("folderId")

        name = d.pop("name")

        author_ids = d.pop("authorIds", UNSET)

        custom_fields: Union[Unset, CustomFields] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(_custom_fields)

        entry_template_id = d.pop("entryTemplateId", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        schema_id = d.pop("schemaId", UNSET)

        entry_create = cls(
            folder_id=folder_id,
            name=name,
            author_ids=author_ids,
            custom_fields=custom_fields,
            entry_template_id=entry_template_id,
            fields=fields,
            schema_id=schema_id,
        )

        return entry_create
