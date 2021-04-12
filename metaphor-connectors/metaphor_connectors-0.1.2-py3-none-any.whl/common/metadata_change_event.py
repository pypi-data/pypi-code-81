# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = metadata_change_event_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class AspectType(Enum):
    DATASET_COMMENT = "DATASET_COMMENT"
    DATASET_DOCUMENTATION = "DATASET_DOCUMENTATION"
    DATASET_DOWNSTREAM = "DATASET_DOWNSTREAM"
    DATASET_SCHEMA = "DATASET_SCHEMA"
    DATASET_STATISTICS = "DATASET_STATISTICS"
    DATASET_UPSTREAM = "DATASET_UPSTREAM"
    GROUP_INFO = "GROUP_INFO"
    OWNERSHIP = "OWNERSHIP"
    PERSON_EDITABLE_INFO = "PERSON_EDITABLE_INFO"
    PROPERTIES = "PROPERTIES"


@dataclass
class AuditStamp:
    actor: Optional[str] = None
    time: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditStamp':
        assert isinstance(obj, dict)
        actor = from_union([from_str, from_none], obj.get("actor"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        return AuditStamp(actor, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["actor"] = from_union([from_str, from_none], self.actor)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        return result


@dataclass
class ObjectID:
    """A class representation of the BSON ObjectId type."""
    """The generation time of this ObjectId instance"""
    generation_time: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ObjectID':
        assert isinstance(obj, dict)
        generation_time = from_union([from_float, from_none], obj.get("generationTime"))
        return ObjectID(generation_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["generationTime"] = from_union([to_float, from_none], self.generation_time)
        return result


@dataclass
class DatasetComment:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    content: Optional[str] = None
    created: Optional[AuditStamp] = None
    created_at: Optional[datetime] = None
    deleted: Optional[AuditStamp] = None
    entity_id: Optional[str] = None
    field: Optional[str] = None
    dataset_comment_id: Optional[str] = None
    latest: Optional[bool] = None
    parent: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetComment':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        content = from_union([from_str, from_none], obj.get("content"))
        created = from_union([AuditStamp.from_dict, from_none], obj.get("created"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted = from_union([AuditStamp.from_dict, from_none], obj.get("deleted"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field = from_union([from_str, from_none], obj.get("field"))
        dataset_comment_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        parent = from_union([from_str, from_none], obj.get("parent"))
        return DatasetComment(id, aspect_type, content, created, created_at, deleted, entity_id, field, dataset_comment_id, latest, parent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["content"] = from_union([from_str, from_none], self.content)
        result["created"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.created)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deleted"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.deleted)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["field"] = from_union([from_str, from_none], self.field)
        result["id"] = from_union([from_str, from_none], self.dataset_comment_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["parent"] = from_union([from_str, from_none], self.parent)
        return result


@dataclass
class FieldDocumentation:
    documentation: Optional[str] = None
    field_path: Optional[str] = None
    tests: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldDocumentation':
        assert isinstance(obj, dict)
        documentation = from_union([from_str, from_none], obj.get("documentation"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        tests = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tests"))
        return FieldDocumentation(documentation, field_path, tests)

    def to_dict(self) -> dict:
        result: dict = {}
        result["documentation"] = from_union([from_str, from_none], self.documentation)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["tests"] = from_union([lambda x: from_list(from_str, x), from_none], self.tests)
        return result


@dataclass
class DatasetDocumentation:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    dataset_documentations: Optional[List[str]] = None
    entity_id: Optional[str] = None
    field_documentations: Optional[List[FieldDocumentation]] = None
    dataset_documentation_id: Optional[str] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetDocumentation':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dataset_documentations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("datasetDocumentations"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_documentations = from_union([lambda x: from_list(FieldDocumentation.from_dict, x), from_none], obj.get("fieldDocumentations"))
        dataset_documentation_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return DatasetDocumentation(id, aspect_type, created_at, dataset_documentations, entity_id, field_documentations, dataset_documentation_id, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["datasetDocumentations"] = from_union([lambda x: from_list(from_str, x), from_none], self.dataset_documentations)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldDocumentations"] = from_union([lambda x: from_list(lambda x: to_class(FieldDocumentation, x), x), from_none], self.field_documentations)
        result["id"] = from_union([from_str, from_none], self.dataset_documentation_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


class DataPlatform(Enum):
    DOCUMENTDB = "DOCUMENTDB"
    DYNAMODB = "DYNAMODB"
    ELASTICSEARCH = "ELASTICSEARCH"
    LOOKER = "LOOKER"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    RDS = "RDS"
    REDIS = "REDIS"
    REDSHIFT = "REDSHIFT"
    S3 = "S3"
    SNOWFLAKE = "SNOWFLAKE"
    UNKNOWN = "UNKNOWN"


@dataclass
class DatasetLogicalID:
    """Identify an entity "logically", besides the system generated UUID.
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring a unique UUID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    name: Optional[str] = None
    platform: Optional[DataPlatform] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetLogicalID':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        platform = from_union([DataPlatform, from_none], obj.get("platform"))
        return DatasetLogicalID(name, platform)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["platform"] = from_union([lambda x: to_enum(DataPlatform, x), from_none], self.platform)
        return result


@dataclass
class DatasetDownstream:
    """DatasetDownstream captures downstream lineages from this dataset"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    datasets: Optional[List[DatasetLogicalID]] = None
    entity_id: Optional[str] = None
    dataset_downstream_id: Optional[str] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetDownstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        datasets = from_union([lambda x: from_list(DatasetLogicalID.from_dict, x), from_none], obj.get("datasets"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dataset_downstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return DatasetDownstream(id, aspect_type, created_at, datasets, entity_id, dataset_downstream_id, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["datasets"] = from_union([lambda x: from_list(lambda x: to_class(DatasetLogicalID, x), x), from_none], self.datasets)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dataset_downstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


class EntityType(Enum):
    DASHBOARD = "DASHBOARD"
    DATASET = "DATASET"
    GROUP = "GROUP"
    PERSON = "PERSON"
    PROJECT = "PROJECT"


@dataclass
class GroupID:
    """Identify an entity "logically", besides the system generated UUID.
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring a unique UUID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    group_name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupID':
        assert isinstance(obj, dict)
        group_name = from_union([from_str, from_none], obj.get("groupName"))
        return GroupID(group_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["groupName"] = from_union([from_str, from_none], self.group_name)
        return result


@dataclass
class GroupOwner:
    group: Optional[GroupID] = None
    role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupOwner':
        assert isinstance(obj, dict)
        group = from_union([GroupID.from_dict, from_none], obj.get("group"))
        role = from_union([from_str, from_none], obj.get("role"))
        return GroupOwner(group, role)

    def to_dict(self) -> dict:
        result: dict = {}
        result["group"] = from_union([lambda x: to_class(GroupID, x), from_none], self.group)
        result["role"] = from_union([from_str, from_none], self.role)
        return result


@dataclass
class PersonID:
    """Identify an entity "logically", besides the system generated UUID.
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring a unique UUID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonID':
        assert isinstance(obj, dict)
        email = from_union([from_str, from_none], obj.get("email"))
        return PersonID(email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_union([from_str, from_none], self.email)
        return result


@dataclass
class PersonOwner:
    person: Optional[PersonID] = None
    role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonOwner':
        assert isinstance(obj, dict)
        person = from_union([PersonID.from_dict, from_none], obj.get("person"))
        role = from_union([from_str, from_none], obj.get("role"))
        return PersonOwner(person, role)

    def to_dict(self) -> dict:
        result: dict = {}
        result["person"] = from_union([lambda x: to_class(PersonID, x), from_none], self.person)
        result["role"] = from_union([from_str, from_none], self.role)
        return result


@dataclass
class Ownership:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    groups: Optional[List[GroupOwner]] = None
    ownership_id: Optional[str] = None
    latest: Optional[bool] = None
    people: Optional[List[PersonOwner]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Ownership':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        groups = from_union([lambda x: from_list(GroupOwner.from_dict, x), from_none], obj.get("groups"))
        ownership_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        people = from_union([lambda x: from_list(PersonOwner.from_dict, x), from_none], obj.get("people"))
        return Ownership(id, aspect_type, created_at, entity_id, groups, ownership_id, latest, people)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["groups"] = from_union([lambda x: from_list(lambda x: to_class(GroupOwner, x), x), from_none], self.groups)
        result["id"] = from_union([from_str, from_none], self.ownership_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["people"] = from_union([lambda x: from_list(lambda x: to_class(PersonOwner, x), x), from_none], self.people)
        return result


@dataclass
class Deprecation:
    deprecated_by: Optional[AuditStamp] = None
    reason: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Deprecation':
        assert isinstance(obj, dict)
        deprecated_by = from_union([AuditStamp.from_dict, from_none], obj.get("deprecatedBy"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return Deprecation(deprecated_by, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["deprecatedBy"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.deprecated_by)
        result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class Properties:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    deprecated: Optional[Deprecation] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    properties_id: Optional[str] = None
    latest: Optional[bool] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deprecated = from_union([Deprecation.from_dict, from_none], obj.get("deprecated"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        properties_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Properties(id, aspect_type, created_at, deprecated, description, entity_id, properties_id, latest, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deprecated"] = from_union([lambda x: to_class(Deprecation, x), from_none], self.deprecated)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.properties_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


@dataclass
class SchemaField:
    description: Optional[str] = None
    field_path: Optional[str] = None
    native_type: Optional[str] = None
    nullable: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SchemaField':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        native_type = from_union([from_str, from_none], obj.get("nativeType"))
        nullable = from_union([from_bool, from_none], obj.get("nullable"))
        return SchemaField(description, field_path, native_type, nullable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["nativeType"] = from_union([from_str, from_none], self.native_type)
        result["nullable"] = from_union([from_bool, from_none], self.nullable)
        return result


class SchemaType(Enum):
    AVRO = "AVRO"
    DYNAMODB = "DYNAMODB"
    JSON = "JSON"
    ORC = "ORC"
    PARQUET = "PARQUET"
    PROTOBUF = "PROTOBUF"
    SCHEMALESS = "SCHEMALESS"
    SQL = "SQL"


@dataclass
class ForeignKey:
    field_path: Optional[str] = None
    parent: Optional[DatasetLogicalID] = None
    parent_field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ForeignKey':
        assert isinstance(obj, dict)
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        parent = from_union([DatasetLogicalID.from_dict, from_none], obj.get("parent"))
        parent_field = from_union([from_str, from_none], obj.get("parentField"))
        return ForeignKey(field_path, parent, parent_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["parent"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.parent)
        result["parentField"] = from_union([from_str, from_none], self.parent_field)
        return result


class MaterializationType(Enum):
    TABLE = "TABLE"
    VIEW = "VIEW"


@dataclass
class SQLSchema:
    foreign_key: Optional[List[ForeignKey]] = None
    materialization: Optional[MaterializationType] = None
    primary_key: Optional[List[str]] = None
    table_schema: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SQLSchema':
        assert isinstance(obj, dict)
        foreign_key = from_union([lambda x: from_list(ForeignKey.from_dict, x), from_none], obj.get("foreignKey"))
        materialization = from_union([MaterializationType, from_none], obj.get("materialization"))
        primary_key = from_union([lambda x: from_list(from_str, x), from_none], obj.get("primaryKey"))
        table_schema = from_union([from_str, from_none], obj.get("tableSchema"))
        return SQLSchema(foreign_key, materialization, primary_key, table_schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["foreignKey"] = from_union([lambda x: from_list(lambda x: to_class(ForeignKey, x), x), from_none], self.foreign_key)
        result["materialization"] = from_union([lambda x: to_enum(MaterializationType, x), from_none], self.materialization)
        result["primaryKey"] = from_union([lambda x: from_list(from_str, x), from_none], self.primary_key)
        result["tableSchema"] = from_union([from_str, from_none], self.table_schema)
        return result


@dataclass
class DatasetSchema:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    fields: Optional[List[SchemaField]] = None
    dataset_schema_id: Optional[str] = None
    last_modified: Optional[AuditStamp] = None
    latest: Optional[bool] = None
    schema_type: Optional[SchemaType] = None
    sql_schema: Optional[SQLSchema] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetSchema':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        fields = from_union([lambda x: from_list(SchemaField.from_dict, x), from_none], obj.get("fields"))
        dataset_schema_id = from_union([from_str, from_none], obj.get("id"))
        last_modified = from_union([AuditStamp.from_dict, from_none], obj.get("lastModified"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        schema_type = from_union([SchemaType, from_none], obj.get("schemaType"))
        sql_schema = from_union([SQLSchema.from_dict, from_none], obj.get("sqlSchema"))
        return DatasetSchema(id, aspect_type, created_at, entity_id, fields, dataset_schema_id, last_modified, latest, schema_type, sql_schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(SchemaField, x), x), from_none], self.fields)
        result["id"] = from_union([from_str, from_none], self.dataset_schema_id)
        result["lastModified"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.last_modified)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["schemaType"] = from_union([lambda x: to_enum(SchemaType, x), from_none], self.schema_type)
        result["sqlSchema"] = from_union([lambda x: to_class(SQLSchema, x), from_none], self.sql_schema)
        return result


@dataclass
class DatasetStatistics:
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    data_size: Optional[float] = None
    entity_id: Optional[str] = None
    dataset_statistics_id: Optional[str] = None
    last_updated: Optional[datetime] = None
    latest: Optional[bool] = None
    record_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetStatistics':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        data_size = from_union([from_float, from_none], obj.get("dataSize"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dataset_statistics_id = from_union([from_str, from_none], obj.get("id"))
        last_updated = from_union([from_datetime, from_none], obj.get("lastUpdated"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        record_count = from_union([from_float, from_none], obj.get("recordCount"))
        return DatasetStatistics(id, aspect_type, created_at, data_size, entity_id, dataset_statistics_id, last_updated, latest, record_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["dataSize"] = from_union([to_float, from_none], self.data_size)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dataset_statistics_id)
        result["lastUpdated"] = from_union([lambda x: x.isoformat(), from_none], self.last_updated)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["recordCount"] = from_union([to_float, from_none], self.record_count)
        return result


@dataclass
class DatasetField:
    dataset: Optional[DatasetLogicalID] = None
    field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetField':
        assert isinstance(obj, dict)
        dataset = from_union([DatasetLogicalID.from_dict, from_none], obj.get("dataset"))
        field = from_union([from_str, from_none], obj.get("field"))
        return DatasetField(dataset, field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataset"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.dataset)
        result["field"] = from_union([from_str, from_none], self.field)
        return result


@dataclass
class FieldMapping:
    destination: Optional[str] = None
    sources: Optional[List[DatasetField]] = None
    transformation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldMapping':
        assert isinstance(obj, dict)
        destination = from_union([from_str, from_none], obj.get("destination"))
        sources = from_union([lambda x: from_list(DatasetField.from_dict, x), from_none], obj.get("sources"))
        transformation = from_union([from_str, from_none], obj.get("transformation"))
        return FieldMapping(destination, sources, transformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["destination"] = from_union([from_str, from_none], self.destination)
        result["sources"] = from_union([lambda x: from_list(lambda x: to_class(DatasetField, x), x), from_none], self.sources)
        result["transformation"] = from_union([from_str, from_none], self.transformation)
        return result


@dataclass
class DatasetUpstream:
    """DatasetUpstream captures upstream lineages from data sources to this dataset"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    executor_url: Optional[str] = None
    field_mappings: Optional[List[FieldMapping]] = None
    dataset_upstream_id: Optional[str] = None
    latest: Optional[bool] = None
    source_code_url: Optional[str] = None
    sources: Optional[List[DatasetLogicalID]] = None
    transformation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetUpstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        executor_url = from_union([from_str, from_none], obj.get("executorUrl"))
        field_mappings = from_union([lambda x: from_list(FieldMapping.from_dict, x), from_none], obj.get("fieldMappings"))
        dataset_upstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        source_code_url = from_union([from_str, from_none], obj.get("sourceCodeUrl"))
        sources = from_union([lambda x: from_list(DatasetLogicalID.from_dict, x), from_none], obj.get("sources"))
        transformation = from_union([from_str, from_none], obj.get("transformation"))
        return DatasetUpstream(id, aspect_type, created_at, entity_id, executor_url, field_mappings, dataset_upstream_id, latest, source_code_url, sources, transformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["executorUrl"] = from_union([from_str, from_none], self.executor_url)
        result["fieldMappings"] = from_union([lambda x: from_list(lambda x: to_class(FieldMapping, x), x), from_none], self.field_mappings)
        result["id"] = from_union([from_str, from_none], self.dataset_upstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["sourceCodeUrl"] = from_union([from_str, from_none], self.source_code_url)
        result["sources"] = from_union([lambda x: from_list(lambda x: to_class(DatasetLogicalID, x), x), from_none], self.sources)
        result["transformation"] = from_union([from_str, from_none], self.transformation)
        return result


@dataclass
class Dataset:
    comments: Optional[List[DatasetComment]] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    documentation: Optional[DatasetDocumentation] = None
    """DatasetDownstream captures downstream lineages from this dataset"""
    downstream: Optional[DatasetDownstream] = None
    entity_type: Optional[EntityType] = None
    id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically", besides the system generated UUID.
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring a unique UUID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[DatasetLogicalID] = None
    ownership: Optional[Ownership] = None
    properties: Optional[Properties] = None
    schema: Optional[DatasetSchema] = None
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    statistics: Optional[DatasetStatistics] = None
    """DatasetUpstream captures upstream lineages from data sources to this dataset"""
    upstream: Optional[DatasetUpstream] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        comments = from_union([lambda x: from_list(DatasetComment.from_dict, x), from_none], obj.get("comments"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        documentation = from_union([DatasetDocumentation.from_dict, from_none], obj.get("documentation"))
        downstream = from_union([DatasetDownstream.from_dict, from_none], obj.get("downstream"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([DatasetLogicalID.from_dict, from_none], obj.get("logicalId"))
        ownership = from_union([Ownership.from_dict, from_none], obj.get("ownership"))
        properties = from_union([Properties.from_dict, from_none], obj.get("properties"))
        schema = from_union([DatasetSchema.from_dict, from_none], obj.get("schema"))
        statistics = from_union([DatasetStatistics.from_dict, from_none], obj.get("statistics"))
        upstream = from_union([DatasetUpstream.from_dict, from_none], obj.get("upstream"))
        return Dataset(comments, created_at, deleted_at, documentation, downstream, entity_type, id, last_modified_at, logical_id, ownership, properties, schema, statistics, upstream)

    def to_dict(self) -> dict:
        result: dict = {}
        result["comments"] = from_union([lambda x: from_list(lambda x: to_class(DatasetComment, x), x), from_none], self.comments)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["documentation"] = from_union([lambda x: to_class(DatasetDocumentation, x), from_none], self.documentation)
        result["downstream"] = from_union([lambda x: to_class(DatasetDownstream, x), from_none], self.downstream)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.logical_id)
        result["ownership"] = from_union([lambda x: to_class(Ownership, x), from_none], self.ownership)
        result["properties"] = from_union([lambda x: to_class(Properties, x), from_none], self.properties)
        result["schema"] = from_union([lambda x: to_class(DatasetSchema, x), from_none], self.schema)
        result["statistics"] = from_union([lambda x: to_class(DatasetStatistics, x), from_none], self.statistics)
        result["upstream"] = from_union([lambda x: to_class(DatasetUpstream, x), from_none], self.upstream)
        return result


@dataclass
class EventHeader:
    app_name: Optional[str] = None
    server: Optional[str] = None
    time: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EventHeader':
        assert isinstance(obj, dict)
        app_name = from_union([from_str, from_none], obj.get("appName"))
        server = from_union([from_str, from_none], obj.get("server"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        return EventHeader(app_name, server, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["appName"] = from_union([from_str, from_none], self.app_name)
        result["server"] = from_union([from_str, from_none], self.server)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        return result


@dataclass
class GroupInfo:
    id: Optional[ObjectID] = None
    admins: Optional[List[PersonID]] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    email: Optional[str] = None
    entity_id: Optional[str] = None
    group_info_id: Optional[str] = None
    latest: Optional[bool] = None
    members: Optional[List[PersonID]] = None
    subgroups: Optional[List[GroupID]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        admins = from_union([lambda x: from_list(PersonID.from_dict, x), from_none], obj.get("admins"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        email = from_union([from_str, from_none], obj.get("email"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        group_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        members = from_union([lambda x: from_list(PersonID.from_dict, x), from_none], obj.get("members"))
        subgroups = from_union([lambda x: from_list(GroupID.from_dict, x), from_none], obj.get("subgroups"))
        return GroupInfo(id, admins, aspect_type, created_at, email, entity_id, group_info_id, latest, members, subgroups)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["admins"] = from_union([lambda x: from_list(lambda x: to_class(PersonID, x), x), from_none], self.admins)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["email"] = from_union([from_str, from_none], self.email)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.group_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["members"] = from_union([lambda x: from_list(lambda x: to_class(PersonID, x), x), from_none], self.members)
        result["subgroups"] = from_union([lambda x: from_list(lambda x: to_class(GroupID, x), x), from_none], self.subgroups)
        return result


@dataclass
class Group:
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    group_info: Optional[GroupInfo] = None
    id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically", besides the system generated UUID.
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring a unique UUID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[GroupID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        group_info = from_union([GroupInfo.from_dict, from_none], obj.get("groupInfo"))
        id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([GroupID.from_dict, from_none], obj.get("logicalId"))
        return Group(created_at, deleted_at, entity_type, group_info, id, last_modified_at, logical_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["groupInfo"] = from_union([lambda x: to_class(GroupInfo, x), from_none], self.group_info)
        result["id"] = from_union([from_str, from_none], self.id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(GroupID, x), from_none], self.logical_id)
        return result


@dataclass
class Person:
    """A person entity represents any individual who is a member of the organization (or beyond)
    and can
    potentially have some relation to the other entities in our application
    """
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    first_name: Optional[str] = None
    id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    last_name: Optional[str] = None
    """Identify an entity "logically", besides the system generated UUID.
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring a unique UUID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[PersonID] = None
    password: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Person':
        assert isinstance(obj, dict)
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        first_name = from_union([from_str, from_none], obj.get("firstName"))
        id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        last_name = from_union([from_str, from_none], obj.get("lastName"))
        logical_id = from_union([PersonID.from_dict, from_none], obj.get("logicalId"))
        password = from_union([from_str, from_none], obj.get("password"))
        return Person(avatar_url, created_at, deleted_at, entity_type, first_name, id, last_modified_at, last_name, logical_id, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["firstName"] = from_union([from_str, from_none], self.first_name)
        result["id"] = from_union([from_str, from_none], self.id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["lastName"] = from_union([from_str, from_none], self.last_name)
        result["logicalId"] = from_union([lambda x: to_class(PersonID, x), from_none], self.logical_id)
        result["password"] = from_union([from_str, from_none], self.password)
        return result


@dataclass
class MetadataChangeEvent:
    dataset: Optional[Dataset] = None
    event_header: Optional[EventHeader] = None
    group: Optional[Group] = None
    """A person entity represents any individual who is a member of the organization (or beyond)
    and can
    potentially have some relation to the other entities in our application
    """
    person: Optional[Person] = None
    tenant: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MetadataChangeEvent':
        assert isinstance(obj, dict)
        dataset = from_union([Dataset.from_dict, from_none], obj.get("dataset"))
        event_header = from_union([EventHeader.from_dict, from_none], obj.get("eventHeader"))
        group = from_union([Group.from_dict, from_none], obj.get("group"))
        person = from_union([Person.from_dict, from_none], obj.get("person"))
        tenant = from_union([from_str, from_none], obj.get("tenant"))
        return MetadataChangeEvent(dataset, event_header, group, person, tenant)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataset"] = from_union([lambda x: to_class(Dataset, x), from_none], self.dataset)
        result["eventHeader"] = from_union([lambda x: to_class(EventHeader, x), from_none], self.event_header)
        result["group"] = from_union([lambda x: to_class(Group, x), from_none], self.group)
        result["person"] = from_union([lambda x: to_class(Person, x), from_none], self.person)
        result["tenant"] = from_union([from_str, from_none], self.tenant)
        return result


def metadata_change_event_from_dict(s: Any) -> MetadataChangeEvent:
    return MetadataChangeEvent.from_dict(s)


def metadata_change_event_to_dict(x: MetadataChangeEvent) -> Any:
    return to_class(MetadataChangeEvent, x)
