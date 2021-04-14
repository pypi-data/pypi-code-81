from typing import Any, Callable, Optional, TypeVar

import typer

from benchling_sdk.benchbots.benchling_store import BenchlingStore, Resource, Schema
from benchling_sdk.benchbots.types.manifest import (
    DropdownDependency,
    NamedResourceDependency,
    SchemaDependency,
)
from benchling_sdk.models import DropdownOption, DropdownSummary

T = TypeVar("T")


def _prompt_until_success(
    initial_value: str, resolver: Callable[[str], Optional[T]], error_prompt: Callable[[str], str]
) -> T:
    value = initial_value
    while True:
        resolved_object = resolver(value)
        if resolved_object:
            return resolved_object
        else:
            value = typer.prompt(error_prompt(value))


def resolve_schema_by_id_or_name(
    benchling_store: BenchlingStore,
    schema_dependency: SchemaDependency,
    initial_id_or_name: str,
) -> Schema:
    # error: Incompatible return value type (got "object", expected "Union[AssayResultSchema...]")
    # I think it might be a MyPy issue; see https://github.com/python/mypy/issues/6898
    return _prompt_until_success(  # type: ignore
        initial_value=initial_id_or_name,
        resolver=lambda id_or_name: benchling_store.get_schema_by_id_or_name(
            schema_dependency.resourceType, id_or_name
        ),
        error_prompt=lambda id_or_name: (
            f'No {schema_dependency.resourceType} found for dependency "{schema_dependency.name}" '
            f'with id or name "{id_or_name}". '
            "Please enter the correct schema's API ID or name"
        ),
    )


def resolve_field_by_id_or_name(
    benchling_store: BenchlingStore,
    schema: Schema,
    initial_id_or_name: str,
    dependency_name: str,
) -> Any:
    return _prompt_until_success(
        initial_value=initial_id_or_name,
        resolver=lambda id_or_name: benchling_store.get_schema_field_by_id_or_name(schema, id_or_name),
        error_prompt=lambda id_or_name: (
            f'No schema field found on schema "{schema.name}" for dependency '
            f'"{dependency_name}" with id or name "{id_or_name}". '
            "Please enter the correct field's API ID or name"
        ),
    )


def resolve_dropdown_by_id_or_name(
    benchling_store: BenchlingStore,
    dropdown_dependency: DropdownDependency,
    initial_id_or_name: str,
) -> DropdownSummary:
    return _prompt_until_success(
        initial_value=initial_id_or_name,
        resolver=benchling_store.get_dropdown_by_id_or_name,
        error_prompt=lambda id_or_name: (
            f'No dropdown found for dependency "{dropdown_dependency.name}" '
            f'with id or name "{id_or_name}". '
            "Please enter the correct dropdown's API ID or name"
        ),
    )


def resolve_option_by_id_or_name(
    benchling_store: BenchlingStore,
    dropdown: DropdownSummary,
    initial_id_or_name: str,
    dependency_name: str,
) -> DropdownOption:
    return _prompt_until_success(
        initial_value=initial_id_or_name,
        resolver=lambda id_or_name: benchling_store.get_dropdown_option_by_id_or_name(
            dropdown.id, id_or_name
        ),
        error_prompt=lambda id_or_name: (
            f'No dropdown option found on dropdown "{dropdown.name}" for dependency '
            f'"{dependency_name}" with id or name "{id_or_name}". '
            "Please enter the correct option's API ID or name"
        ),
    )


def resolve_resource_by_id_or_name(
    benchling_store: BenchlingStore,
    resource_dependency: NamedResourceDependency,
    initial_id_or_name: str,
) -> Resource:
    # error: Incompatible return value type (got "object", expected "Union[AaSequence...]")
    # I think it might be a MyPy issue; see https://github.com/python/mypy/issues/6898
    return _prompt_until_success(  # type: ignore
        initial_value=initial_id_or_name,
        resolver=lambda id_or_name: benchling_store.get_resource_by_id_or_name(
            resource_dependency.resourceType, id_or_name
        ),
        error_prompt=lambda id_or_name: (
            f'No {resource_dependency.resourceType} found for dependency "{resource_dependency.name}" '
            f'with id or name "{id_or_name}". '
            f"Please enter the correct {resource_dependency.resourceType}'s API ID or name"
        ),
    )
