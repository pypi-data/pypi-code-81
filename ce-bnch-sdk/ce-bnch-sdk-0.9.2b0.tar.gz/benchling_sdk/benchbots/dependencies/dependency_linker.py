from typing import cast, Optional

import typer

from benchling_sdk.benchbots.benchling_store import BenchlingStore, Schema
from benchling_sdk.benchbots.dependencies.dependency_resolution import (
    resolve_dropdown_by_id_or_name,
    resolve_field_by_id_or_name,
    resolve_option_by_id_or_name,
    resolve_resource_by_id_or_name,
    resolve_schema_by_id_or_name,
)
from benchling_sdk.benchbots.helpers.find import find
from benchling_sdk.benchbots.types.dependency_links import (
    DependencyLinks,
    DropdownLink,
    DropdownOptionLink,
    NamedResourceLink,
    SchemaFieldLink,
    SchemaLink,
    UnnamedResourceLink,
)
from benchling_sdk.benchbots.types.manifest import (
    AUTOLINKED_RESOURCE_TYPES,
    BaseDependency,
    DropdownDependency,
    Manifest,
    NamedResourceDependency,
    SchemaDependency,
    UnnamedResourceDependency,
)
from benchling_sdk.models import DropdownSummary


class DependencyLinker:
    benchling_store: BenchlingStore

    def __init__(self, benchling_store: BenchlingStore) -> None:
        self.benchling_store = benchling_store

    def link_dependencies(
        self,
        dependency_links: Optional[DependencyLinks],
        manifest: Manifest,
    ) -> DependencyLinks:
        if not dependency_links:
            dependency_links = DependencyLinks(dependencies=[])
        self.update_dependency_links(dependency_links, manifest)
        return dependency_links

    def update_dependency_links(self, dependency_links: DependencyLinks, manifest: Manifest) -> None:
        if manifest.dependencies:
            for dependency in manifest.dependencies:
                existing_link = find(dependency_links.dependencies, lambda x: x.name == dependency.name)

                if isinstance(dependency, SchemaDependency):
                    if existing_link:
                        assert isinstance(existing_link, SchemaLink)
                        self.update_schema_link(dependency, existing_link)
                    else:
                        dependency_links.dependencies.append(self.link_schema(dependency))
                elif isinstance(dependency, DropdownDependency):
                    if existing_link:
                        assert isinstance(existing_link, DropdownLink)
                        self.update_dropdown_link(dependency, existing_link)
                    else:
                        dependency_links.dependencies.append(self.link_dropdown(dependency))
                elif isinstance(dependency, NamedResourceDependency):
                    if dependency.resourceType in AUTOLINKED_RESOURCE_TYPES:
                        if existing_link:
                            assert isinstance(existing_link, NamedResourceLink)
                            self.update_resource_link(dependency, existing_link)
                        else:
                            dependency_links.dependencies.append(self.link_resource(dependency))
                    else:
                        if existing_link:
                            typer.secho(
                                f'Skipping dependency "{dependency.name}" '
                                f'because it is of type "{dependency.resourceType}"',
                                fg="red",
                            )
                        else:
                            resource_id = typer.prompt(
                                f'Dependency "{dependency.name}" cannot be auto-linked '
                                f'because it is of type "{dependency.resourceType}".\n'
                                "Please enter the resource's API ID"
                            )
                            resource_name = typer.prompt("Please enter the resource's name")
                            dependency_links.dependencies.append(
                                NamedResourceLink(
                                    name=dependency.name,
                                    resourceId=resource_id,
                                    resourceName=resource_name,
                                )
                            )
                elif isinstance(dependency, UnnamedResourceDependency):
                    if existing_link:
                        typer.secho(
                            f'Skipping dependency "{dependency.name}" '
                            f'because it is of type "{dependency.resourceType}"',
                            fg="red",
                        )
                    else:
                        resource_id = typer.prompt(
                            f'Dependency "{dependency.name}" cannot be auto-linked '
                            f'because it is of type "{dependency.resourceType}".\n'
                            "Please enter the resource's API ID"
                        )
                        dependency_links.dependencies.append(
                            UnnamedResourceLink(
                                name=dependency.name,
                                resourceId=resource_id,
                            )
                        )
                else:
                    raise NotImplementedError(f"Unsupported dependency={dependency}")

    def update_schema_link(self, schema_dependency: SchemaDependency, schema_link: SchemaLink) -> None:
        schema = resolve_schema_by_id_or_name(
            benchling_store=self.benchling_store,
            schema_dependency=schema_dependency,
            initial_id_or_name=schema_link.resourceId,
        )
        schema_link.resourceId = schema.id
        schema_link.resourceName = cast(str, schema.name)

        if schema_dependency.fieldDefinitions:
            for field in schema_dependency.fieldDefinitions:
                existing_link = find(schema_link.fieldDefinitions, lambda x: x.name == field.name)

                if existing_link:
                    self.update_field_link(schema, existing_link)
                else:
                    schema_link.fieldDefinitions.append(self.link_field(schema, field))

    def update_field_link(self, schema: Schema, field_link: SchemaFieldLink) -> None:
        field = resolve_field_by_id_or_name(
            benchling_store=self.benchling_store,
            schema=schema,
            initial_id_or_name=field_link.resourceId,
            dependency_name=field_link.name,
        )
        field_link.resourceId = field.id
        field_link.resourceName = field.name

    def link_schema(self, schema_dependency: SchemaDependency) -> SchemaLink:
        schema = resolve_schema_by_id_or_name(
            benchling_store=self.benchling_store,
            schema_dependency=schema_dependency,
            initial_id_or_name=schema_dependency.name,
        )
        schema_fields = (
            [
                self.link_field(schema, field_dependency)
                for field_dependency in schema_dependency.fieldDefinitions
            ]
            if schema_dependency.fieldDefinitions
            else []
        )
        typer.echo(f"Linking {schema_dependency.name} to {schema.id}")
        return SchemaLink(
            name=schema_dependency.name,
            resourceId=schema.id,
            resourceName=cast(str, schema.name),
            fieldDefinitions=schema_fields,
        )

    def link_field(self, schema: Schema, field_dependency: BaseDependency) -> SchemaFieldLink:
        field = resolve_field_by_id_or_name(
            benchling_store=self.benchling_store,
            schema=schema,
            initial_id_or_name=field_dependency.name,
            dependency_name=field_dependency.name,
        )
        typer.echo(f"Linking {field_dependency.name} to {field.id}")
        return SchemaFieldLink(
            name=field_dependency.name,
            resourceId=field.id,
            resourceName=cast(str, field.name),
        )

    def update_dropdown_link(
        self, dropdown_dependency: DropdownDependency, dropdown_link: DropdownLink
    ) -> None:
        dropdown = resolve_dropdown_by_id_or_name(
            benchling_store=self.benchling_store,
            dropdown_dependency=dropdown_dependency,
            initial_id_or_name=dropdown_link.resourceId,
        )
        dropdown_link.resourceId = dropdown.id
        dropdown_link.resourceName = cast(str, dropdown.name)

        if dropdown_dependency.options:
            for option in dropdown_dependency.options:
                existing_link = find(dropdown_link.options, lambda x: x.name == option.name)

                if existing_link:
                    self.update_option_link(dropdown, existing_link)
                else:
                    dropdown_link.options.append(self.link_option(dropdown, option))

    def update_option_link(self, parent_dropdown: DropdownSummary, option_link: DropdownOptionLink) -> None:
        option = resolve_option_by_id_or_name(
            benchling_store=self.benchling_store,
            dropdown=parent_dropdown,
            initial_id_or_name=option_link.resourceId,
            dependency_name=option_link.name,
        )
        option_link.resourceId = option.id
        option_link.resourceName = cast(str, option.name)

    def link_dropdown(self, dropdown_dependency: DropdownDependency) -> DropdownLink:
        dropdown = resolve_dropdown_by_id_or_name(
            benchling_store=self.benchling_store,
            dropdown_dependency=dropdown_dependency,
            initial_id_or_name=dropdown_dependency.name,
        )
        options = (
            [
                self.link_option(dropdown, option_dependency)
                for option_dependency in dropdown_dependency.options
            ]
            if dropdown_dependency.options
            else []
        )
        typer.echo(f"Linking {dropdown_dependency.name} to {dropdown.id}")
        return DropdownLink(
            name=dropdown_dependency.name,
            resourceId=dropdown.id,
            resourceName=cast(str, dropdown.name),
            options=options,
        )

    def link_option(
        self, parent_dropdown: DropdownSummary, option_dependency: BaseDependency
    ) -> DropdownOptionLink:
        option = resolve_option_by_id_or_name(
            benchling_store=self.benchling_store,
            dropdown=parent_dropdown,
            initial_id_or_name=option_dependency.name,
            dependency_name=option_dependency.name,
        )
        typer.echo(f"Linking {option_dependency.name} to {option.id}")
        return DropdownOptionLink(
            name=option_dependency.name,
            resourceId=option.id,
            resourceName=cast(str, option.name),
        )

    def update_resource_link(
        self, resource_dependency: NamedResourceDependency, resource_link: NamedResourceLink
    ) -> None:
        resource = resolve_resource_by_id_or_name(
            benchling_store=self.benchling_store,
            resource_dependency=resource_dependency,
            initial_id_or_name=resource_link.resourceId,
        )
        resource_link.resourceId = cast(str, resource.id)
        resource_link.resourceName = cast(str, resource.name)

    def link_resource(self, resource_dependency: NamedResourceDependency) -> NamedResourceLink:
        resource = resolve_resource_by_id_or_name(
            benchling_store=self.benchling_store,
            resource_dependency=resource_dependency,
            initial_id_or_name=resource_dependency.name,
        )
        typer.echo(f"Linking {resource_dependency.name} to {resource.id}")
        return NamedResourceLink(
            name=resource_dependency.name,
            resourceId=cast(str, resource.id),
            resourceName=cast(str, resource.name),
        )
