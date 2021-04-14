from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.box_schema_container_schema import BoxSchemaContainerSchema
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="BoxSchema")


@attr.s(auto_attribs=True)
class BoxSchema:
    """  """

    field_definitions: List[SchemaField]
    id: str
    name: str
    type: str
    container_schema: Union[Unset, None, BoxSchemaContainerSchema] = UNSET
    height: Union[Unset, float] = UNSET
    width: Union[Unset, float] = UNSET
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
        container_schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.container_schema, Unset):
            container_schema = self.container_schema.to_dict() if self.container_schema else None

        height = self.height
        width = self.width
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
        if container_schema is not UNSET:
            field_dict["containerSchema"] = container_schema
        if height is not UNSET:
            field_dict["height"] = height
        if width is not UNSET:
            field_dict["width"] = width
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

        container_schema = None
        _container_schema = d.pop("containerSchema", UNSET)
        if _container_schema is not None and not isinstance(_container_schema, Unset):
            container_schema = BoxSchemaContainerSchema.from_dict(_container_schema)

        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        box_schema = cls(
            field_definitions=field_definitions,
            id=id,
            name=name,
            type=type,
            container_schema=container_schema,
            height=height,
            width=width,
            prefix=prefix,
            registry_id=registry_id,
        )

        return box_schema
