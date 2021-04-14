from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchSchema")


@attr.s(auto_attribs=True)
class BatchSchema:
    """  """

    field_definitions: List[SchemaField]
    id: str
    name: str
    type: str
    entity_schema_id: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field_definitions = []
        for field_definitions_item_data in self.field_definitions:
            field_definitions_item = field_definitions_item_data.to_dict()

            field_definitions.append(field_definitions_item)

        id = self.id
        name = self.name
        type = self.type
        entity_schema_id = self.entity_schema_id
        prefix = self.prefix
        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fieldDefinitions": field_definitions,
                "id": id,
                "name": name,
                "type": type,
            }
        )
        if entity_schema_id is not UNSET:
            field_dict["entitySchemaId"] = entity_schema_id
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions")
        for field_definitions_item_data in _field_definitions:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        id = d.pop("id")

        name = d.pop("name")

        type = d.pop("type")

        entity_schema_id = d.pop("entitySchemaId", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        batch_schema = cls(
            field_definitions=field_definitions,
            id=id,
            name=name,
            type=type,
            entity_schema_id=entity_schema_id,
            prefix=prefix,
            registry_id=registry_id,
        )

        return batch_schema
