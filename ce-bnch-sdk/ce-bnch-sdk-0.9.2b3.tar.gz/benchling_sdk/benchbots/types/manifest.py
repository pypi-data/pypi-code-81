from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, List, Optional, Type, TypeVar, Union

from dataclasses_json import dataclass_json
from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_jsonschema.type_defs import JsonDict
from typing_extensions import Literal
import yaml

from benchling_sdk.benchbots.helpers.case_conversion import to_pascal_case, to_snake_case
from benchling_sdk.models import (
    AssayResult,
    AssayRun,
    Box,
    Container,
    CustomEntity,
    Entry,
    Location,
    Plate,
    Request,
)


class SchemaType(str, Enum):
    ENTITY_SCHEMA = "entity-schema"
    CONTAINER_SCHEMA = "container-schema"
    PLATE_SCHEMA = "plate-schema"
    BOX_SCHEMA = "box-schema"
    LOCATION_SCHEMA = "location-schema"
    ASSAY_RESULT_SCHEMA = "assay-result-schema"
    ASSAY_RUN_SCHEMA = "assay-run-schema"
    REQUEST_SCHEMA = "request-schema"
    TASK_SCHEMA = "task-schema"
    ENTRY_SCHEMA = "entry-schema"


SCHEMA_TYPE_TO_INSTANCE = {
    SchemaType.ENTITY_SCHEMA: CustomEntity,
    SchemaType.CONTAINER_SCHEMA: Container,
    SchemaType.PLATE_SCHEMA: Plate,
    SchemaType.BOX_SCHEMA: Box,
    SchemaType.LOCATION_SCHEMA: Location,
    SchemaType.ASSAY_RESULT_SCHEMA: AssayResult,
    SchemaType.ASSAY_RUN_SCHEMA: AssayRun,
    SchemaType.REQUEST_SCHEMA: Request,
    SchemaType.ENTRY_SCHEMA: Entry,
}


class NamedResourceType(str, Enum):
    AA_SEQUENCE = "aa-sequence"
    BOX = "box"
    CONTAINER = "container"
    CUSTOM_ENTITY = "custom-entity"
    DNA_ALIGNMENT = "dna-alignment"  # Cannot be auto-linked because there is no SDK support
    DNA_OLIGO = "dna-oligo"  # Cannot be auto-linked because there is no SDK support
    DNA_SEQUENCE = "dna-sequence"
    ENTRY = "entry"
    FOLDER = "folder"
    LABEL_PRINTER = "label-printer"
    LABEL_TEMPLATE = "label-template"
    LOCATION = "location"
    PLATE = "plate"
    PROJECT = "project"
    REGISTRY = "registry"
    WORKFLOW = "workflow"  # Cannot be auto-linked because there is no SDK support


class UnnamedResourceType(str, Enum):
    ASSAY_RESULT = "assay-result"
    ASSAY_RUN = "assay-run"
    AUTOMATION_INPUT_GENERATOR = "automation-input-generator"
    AUTOMATION_OUTPUT_PROCESSOR = "automation-output-processor"
    BLOB = "blob"
    REQUEST = "request"


AUTOLINKED_RESOURCE_TYPES = [
    NamedResourceType.AA_SEQUENCE,
    NamedResourceType.BOX,
    NamedResourceType.CONTAINER,
    NamedResourceType.CUSTOM_ENTITY,
    NamedResourceType.DNA_SEQUENCE,
    NamedResourceType.ENTRY,
    NamedResourceType.FOLDER,
    NamedResourceType.LABEL_PRINTER,
    NamedResourceType.LABEL_TEMPLATE,
    NamedResourceType.LOCATION,
    NamedResourceType.PLATE,
    NamedResourceType.PROJECT,
    NamedResourceType.REGISTRY,
]


@dataclass_json
class ManifestComponent(JsonSchemaMixin):
    pass


class NamedManifestComponent(ManifestComponent):
    name: str

    @property
    def pascal_case_name(self) -> str:
        return to_pascal_case(self.name)

    @property
    def snake_case_name(self) -> str:
        return to_snake_case(self.name)


@dataclass
class BaseDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    name: str
    description: Optional[str] = None
    is_resource_named: ClassVar[bool] = True


@dataclass
class SchemaDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    resourceType: SchemaType
    description: Optional[str] = None
    fieldDefinitions: Optional[List[BaseDependency]] = None
    is_resource_named: ClassVar[bool] = True

    @property
    def instance_pascal_case_name(self) -> str:
        return SCHEMA_TYPE_TO_INSTANCE[self.resourceType].__name__

    @property
    def instance_snake_case_name(self) -> str:
        return to_snake_case(self.instance_pascal_case_name)


@dataclass
class DropdownDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    resourceType: Literal["dropdown"]
    description: Optional[str] = None
    options: Optional[List[BaseDependency]] = None
    is_resource_named: ClassVar[bool] = True


@dataclass
class NamedResourceDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str
    resourceType: NamedResourceType
    description: Optional[str] = None
    is_resource_named: ClassVar[bool] = True


@dataclass
class UnnamedResourceDependency(NamedManifestComponent, allow_additional_props=False):  # type: ignore
    # Unfortunately dataclasses-jsonschema does not support inheritance with `allow_additional_props=False`.
    name: str  # The dependency still has a name, but the resource itself does not.
    resourceType: UnnamedResourceType
    description: Optional[str] = None
    is_resource_named: ClassVar[bool] = False


@dataclass
class ManifestInfo(ManifestComponent, allow_additional_props=False):  # type: ignore
    name: str
    version: str
    description: Optional[str] = None


T = TypeVar("T", bound="Manifest")


@dataclass
class _Manifest(ManifestComponent, allow_additional_props=False):  # type: ignore
    manifestFormatVersion: Literal[1]
    info: ManifestInfo
    dependencies: Optional[
        List[Union[SchemaDependency, DropdownDependency, NamedResourceDependency, UnnamedResourceDependency]]
    ]


class Manifest(_Manifest):
    @classmethod
    def from_dict(cls: Type[T], data: JsonDict, validate=True, validate_enums: bool = True) -> T:
        # from_dict is not supported properly by dataclasses-json because it's a union type.
        # See https://github.com/lidatong/dataclasses-json/issues/222.
        manifest = super().from_dict(data)
        if manifest.dependencies:
            for i, dependency in enumerate(manifest.dependencies):
                assert isinstance(dependency, dict)
                if dependency["resourceType"] == "dropdown":
                    manifest.dependencies[i] = DropdownDependency.from_dict(dependency)
                elif dependency["resourceType"] in [schema_type.value for schema_type in SchemaType]:
                    manifest.dependencies[i] = SchemaDependency.from_dict(dependency)
                elif dependency["resourceType"] in [
                    resource_type.value for resource_type in NamedResourceType
                ]:
                    manifest.dependencies[i] = NamedResourceDependency.from_dict(dependency)
                else:
                    manifest.dependencies[i] = UnnamedResourceDependency.from_dict(dependency)
        return manifest

    @classmethod
    def from_file(cls: Type[T], file_path: str) -> T:
        with open(file_path) as f:
            manifest_yaml = f.read()
        manifest_dict = yaml.load(manifest_yaml, Loader=yaml.SafeLoader)
        return cls.from_dict(manifest_dict)
