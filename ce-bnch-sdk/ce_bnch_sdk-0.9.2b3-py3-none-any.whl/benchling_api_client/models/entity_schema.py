from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.entity_schema_constraint import EntitySchemaConstraint
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntitySchema")


@attr.s(auto_attribs=True)
class EntitySchema:
    """  """

    field_definitions: List[SchemaField]
    id: str
    name: str
    type: str
    constraint: Union[Unset, None, EntitySchemaConstraint] = UNSET
    containable_type: Union[Unset, str] = UNSET
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
        constraint: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.constraint, Unset):
            constraint = self.constraint.to_dict() if self.constraint else None

        containable_type = self.containable_type
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
        if constraint is not UNSET:
            field_dict["constraint"] = constraint
        if containable_type is not UNSET:
            field_dict["containableType"] = containable_type
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

        constraint = None
        _constraint = d.pop("constraint", UNSET)
        if _constraint is not None and not isinstance(_constraint, Unset):
            constraint = EntitySchemaConstraint.from_dict(_constraint)

        containable_type = d.pop("containableType", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        entity_schema = cls(
            field_definitions=field_definitions,
            id=id,
            name=name,
            type=type,
            constraint=constraint,
            containable_type=containable_type,
            prefix=prefix,
            registry_id=registry_id,
        )

        return entity_schema
