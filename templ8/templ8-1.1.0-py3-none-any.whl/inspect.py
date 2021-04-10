from typing import Any, Dict, List

from .exceptions import (
    InvalidFolderRename,
    MissingCollections,
    MissingIncludes,
    MissingRenderContext,
)
from .models.collection import Collection
from .models.inputs import Inputs
from .models.reporter import Reporter
from .utils.paths import path_head


def inspect_state(
    inputs: Inputs,
    collections: List[Collection],
    schema: Dict[str, Any],
    render_context: Dict[str, Any],
    reporter: Reporter,
) -> None:
    collection_names = [
        path_head(collection.path) for collection in collections
    ]

    static_file_names = [
        path_head(static_file)
        for collection in collections
        for static_file in collection.static_files
    ]

    template_names = [
        path_head(template.output_path)
        for collection in collections
        for template in collection.templates
    ]

    rename_tokens = [
        rename_token
        for collection in collections
        for rename_token in collection.dynamic_folders.values()
    ]

    missing_includes = set(inputs.includes) - (
        set(static_file_names) | set(template_names)
    )

    missing_collections = set(inputs.collections) - set(
        collection_names
    )

    required_context = set(schema["required"]) | set(rename_tokens)
    missing_context = required_context - set(render_context)

    reporter.show_state(
        inputs,
        collections,
        render_context,
        required_context,
    )

    reporter.show_schema(schema)

    if missing_collections:
        raise MissingCollections(missing_collections)

    if missing_includes:
        raise MissingIncludes(missing_includes)

    if missing_context:
        raise MissingRenderContext(missing_context)

    for rename_token in rename_tokens:
        rename = render_context[rename_token]

        if not isinstance(rename, str) or len(rename) == 0:
            raise InvalidFolderRename(rename_token)
