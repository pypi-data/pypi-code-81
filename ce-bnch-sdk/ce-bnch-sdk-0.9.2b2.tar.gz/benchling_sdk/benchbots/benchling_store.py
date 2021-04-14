from http import HTTPStatus
from typing import Any, cast, Dict, Iterable, List, Optional, Union

import typer

from benchling_sdk.benchbots.helpers.find import find, find_by_id_or_name
from benchling_sdk.benchbots.types.manifest import NamedResourceType, SchemaType
from benchling_sdk.benchling import Benchling
from benchling_sdk.errors import BenchlingError
from benchling_sdk.models import (
    AaSequence,
    AssayResultSchema,
    AssayRunSchema,
    Box,
    BoxSchema,
    Container,
    CustomEntity,
    DnaAlignment,
    DnaSequence,
    DropdownOption,
    DropdownSummary,
    EntitySchema,
    Entry,
    EntrySchemaDetailed,
    Folder,
    LabelTemplate,
    Location,
    Plate,
    PlateSchema,
    Printer,
    Project,
    Registry,
    RequestSchema,
    Schema as BaseSchema,
)
from benchling_sdk.services.base_service import BaseService

Schema = Union[
    AssayResultSchema,
    AssayRunSchema,
    BoxSchema,
    EntitySchema,
    EntrySchemaDetailed,
    PlateSchema,
    RequestSchema,
    BaseSchema,
]

Resource = Union[
    AaSequence,
    Box,
    Container,
    CustomEntity,
    DnaAlignment,
    DnaSequence,
    Entry,
    Folder,
    LabelTemplate,
    Location,
    Plate,
    Printer,
    Project,
    Registry,
]


class BenchlingStore:
    _benchling: Benchling
    _schemas: Dict[SchemaType, List[Schema]]
    _dropdowns: Optional[List[DropdownSummary]]
    _dropdown_options_by_dropdown_id: Dict[str, List[DropdownOption]]

    def __init__(self, benchling: Benchling) -> None:
        self._benchling = benchling
        self._schemas = {}
        self._dropdowns = None
        self._dropdown_options_by_dropdown_id = {}

    def _fetch_schema_pages(self, schema_type: SchemaType) -> Iterable[Iterable[Schema]]:
        schema_type_to_service = {
            SchemaType.ENTITY_SCHEMA: self._benchling.schemas.entities,
            SchemaType.CONTAINER_SCHEMA: self._benchling.schemas.containers,
            SchemaType.PLATE_SCHEMA: self._benchling.schemas.plates,
            SchemaType.BOX_SCHEMA: self._benchling.schemas.boxes,
            SchemaType.LOCATION_SCHEMA: self._benchling.schemas.locations,
            SchemaType.ASSAY_RESULT_SCHEMA: self._benchling.schemas.assay_results,
            SchemaType.ASSAY_RUN_SCHEMA: self._benchling.schemas.assay_runs,
            SchemaType.REQUEST_SCHEMA: self._benchling.schemas.requests,
            SchemaType.ENTRY_SCHEMA: self._benchling.schemas.entries,
        }
        # "BaseService" has no attribute "list"
        return schema_type_to_service[schema_type].list()  # type: ignore

    def get_schemas(self, schema_type: SchemaType) -> List[Schema]:
        if schema_type not in self._schemas:
            typer.echo(f"Fetching schemas with schema_type={schema_type}")
            self._schemas[schema_type] = [
                schema for page in self._fetch_schema_pages(schema_type) for schema in page
            ]
        return self._schemas[schema_type]

    def get_schema_by_id_or_name(self, schema_type: SchemaType, id_or_name: str) -> Optional[Schema]:
        return find_by_id_or_name(self.get_schemas(schema_type), id_or_name)

    def get_schema_field_by_id_or_name(self, schema: Schema, id_or_name: str) -> Any:
        return find_by_id_or_name(schema.field_definitions, id_or_name)  # type: ignore

    def get_dropdowns(self) -> List[DropdownSummary]:
        if self._dropdowns is None:
            typer.echo("Fetching dropdowns")
            self._dropdowns = [
                dropdown for page in self._benchling.schemas.dropdowns.list() for dropdown in page
            ]
        return self._dropdowns

    def get_dropdown_by_id_or_name(self, id_or_name: str) -> Optional[DropdownSummary]:
        return find_by_id_or_name(self.get_dropdowns(), id_or_name)

    def get_dropdown_options(self, dropdown_id: str) -> List[DropdownOption]:
        if dropdown_id not in self._dropdown_options_by_dropdown_id:
            typer.echo(f"Fetching dropdown options for dropdown {dropdown_id}")
            self._dropdown_options_by_dropdown_id[dropdown_id] = cast(
                List[DropdownOption], self._benchling.schemas.dropdowns.get_by_id(dropdown_id).options
            )
        return self._dropdown_options_by_dropdown_id[dropdown_id]

    def get_dropdown_option_by_id_or_name(
        self, dropdown_id: str, id_or_name: str
    ) -> Optional[DropdownOption]:
        return find_by_id_or_name(self.get_dropdown_options(dropdown_id), id_or_name)

    def _resource_service(self, resource_type: NamedResourceType) -> BaseService:
        resource_type_to_service = {
            NamedResourceType.AA_SEQUENCE: self._benchling.aa_sequences,
            NamedResourceType.BOX: self._benchling.inventory.boxes,
            NamedResourceType.CONTAINER: self._benchling.inventory.containers,
            NamedResourceType.CUSTOM_ENTITY: self._benchling.custom_entities,
            NamedResourceType.DNA_SEQUENCE: self._benchling.dna_sequences,
            NamedResourceType.ENTRY: self._benchling.notebook,
            NamedResourceType.FOLDER: self._benchling.folders,
            NamedResourceType.LABEL_PRINTER: self._benchling.inventory.labels,
            NamedResourceType.LABEL_TEMPLATE: self._benchling.inventory.labels,
            NamedResourceType.LOCATION: self._benchling.inventory.locations,
            NamedResourceType.PLATE: self._benchling.inventory.plates,
            NamedResourceType.PROJECT: self._benchling.projects,
            NamedResourceType.REGISTRY: self._benchling.registry,
        }
        if resource_type in resource_type_to_service:
            return resource_type_to_service[resource_type]
        else:
            raise NotImplementedError(
                f'The dependency linker does not yet support resources of type "{resource_type}".'
            )

    def get_resource(self, resource_type: NamedResourceType, resource_id: str) -> Optional[Resource]:
        typer.echo(f'Fetching {resource_type} with id "{resource_id}"')
        if resource_type == NamedResourceType.ENTRY:
            try:
                return self._benchling.notebook.get_entry_by_id(resource_id)
            except BenchlingError as e:
                if e.status_code == HTTPStatus.NOT_FOUND:
                    return None
                else:
                    raise e
        elif resource_type == NamedResourceType.LABEL_PRINTER:
            registries = self._benchling.registry.registries()
            return find(
                [
                    printer
                    for registry in registries
                    for printer in self._benchling.inventory.labels.printers(registry.id)
                ],
                lambda x: x.id == resource_id,
            )
        elif resource_type == NamedResourceType.LABEL_TEMPLATE:
            registries = self._benchling.registry.registries()
            return find(
                [
                    template
                    for registry in registries
                    for template in self._benchling.inventory.labels.templates(registry.id)
                ],
                lambda x: x.id == resource_id,
            )
        elif resource_type == NamedResourceType.REGISTRY:
            return find(self._benchling.registry.registries(), lambda x: x.id == resource_id)
        else:
            try:
                # "BaseService" has no attribute "get_by_id"
                return self._resource_service(resource_type).get_by_id(resource_id)  # type: ignore
            except BenchlingError as e:
                if e.status_code == HTTPStatus.NOT_FOUND:
                    return None
                else:
                    raise e

    def _get_resources_by_name(self, resource_type: NamedResourceType, resource_name: str) -> List[Resource]:
        typer.echo(f'Fetching {resource_type} with name "{resource_name}"')
        if resource_type == NamedResourceType.ENTRY:
            return [
                resource
                for page in self._benchling.notebook.list_entries(name=resource_name)
                for resource in page
            ]
        elif resource_type == NamedResourceType.FOLDER:
            return [
                resource
                for page in self._benchling.folders.list(name_includes=resource_name)
                for resource in page
            ]
        elif resource_type == NamedResourceType.LABEL_PRINTER:
            registries = self._benchling.registry.registries()
            return [
                printer
                for registry in registries
                for printer in self._benchling.inventory.labels.printers(registry.id)
            ]
        elif resource_type == NamedResourceType.LABEL_TEMPLATE:
            registries = self._benchling.registry.registries()
            return [
                template
                for registry in registries
                for template in self._benchling.inventory.labels.templates(registry.id)
            ]
        elif resource_type == NamedResourceType.PROJECT:
            return [resource for page in self._benchling.projects.list() for resource in page]
        elif resource_type == NamedResourceType.REGISTRY:
            # Copy list to avoid type error because lists are invariant
            return list(self._benchling.registry.registries())
        else:
            return [
                resource
                # "BaseService" has no attribute "list"
                for page in self._resource_service(resource_type).list(name=resource_name)  # type: ignore
                for resource in page
            ]

    def get_resource_by_name(
        self, resource_type: NamedResourceType, resource_name: str
    ) -> Optional[Resource]:
        return find(
            self._get_resources_by_name(resource_type, resource_name), lambda x: x.name == resource_name
        )

    def get_resource_by_id_or_name(
        self, resource_type: NamedResourceType, id_or_name: str
    ) -> Optional[Resource]:
        return self.get_resource(resource_type, id_or_name) or self.get_resource_by_name(
            resource_type, id_or_name
        )
