from dataclasses import dataclass
from typing import Any, Dict, List, Type, TypeVar

from templ8.models.collection import Collection
from templ8.models.inputs import Inputs
from templ8.models.reporter import Reporter
from templ8.services.dynamic import dynamic_render_context
from templ8.services.exceptions import (
    InvalidFolderRename,
    MissingCollections,
    MissingIncludes,
    MissingRenderContext,
)
from templ8.services.jinja import combine_schemas
from templ8.utils.dicts import merge_dicts
from templ8.utils.lists import merge_lists
from templ8.utils.paths import path_head

T = TypeVar("T", bound="State")  #  pylint: disable = C0103


@dataclass
class State:
    inputs: Inputs
    collections: List[Collection]
    protected: List[str]
    schema: Dict[str, Any]
    render_context: Dict[str, Any]

    @classmethod
    def load(
        cls: Type[T],
        input_file: str,
    ) -> T:
        inputs = Inputs.from_file(input_file)

        collections = Collection.gather(
            inputs.collections,
            inputs.includes,
            inputs.collection_sources,
        )

        protected = merge_lists(
            inputs.protected,
            *[
                collection.default_protected
                for collection in collections
            ],
        )

        schema = merge_dicts(
            {"required": []}, combine_schemas(collections)
        )

        render_context = merge_dicts(
            dynamic_render_context,
            *[
                collection.default_variables
                for collection in collections
            ],
            inputs.render_context,
        )

        return cls(
            inputs, collections, protected, schema, render_context
        )

    def inspect(self, reporter: Reporter) -> None:
        collection_names = [
            path_head(collection.path)
            for collection in self.collections
        ]

        static_file_names = [
            path_head(static_file)
            for collection in self.collections
            for static_file in collection.static_files
        ]

        template_names = [
            path_head(template.output_path)
            for collection in self.collections
            for template in collection.templates
        ]

        rename_tokens = [
            rename_token
            for collection in self.collections
            for rename_token in collection.dynamic_folders.values()
        ]

        missing_includes = set(self.inputs.includes) - (
            set(static_file_names) | set(template_names)
        )

        missing_collections = set(self.inputs.collections) - set(
            collection_names
        )

        required_context = set(self.schema["required"]) | set(
            rename_tokens
        )
        missing_context = required_context - set(self.render_context)

        reporter.show_state(
            self.inputs,
            self.collections,
            self.render_context,
            required_context,
        )

        reporter.show_schema(self.schema)

        if missing_collections:
            raise MissingCollections(missing_collections)

        if missing_includes:
            raise MissingIncludes(missing_includes)

        if missing_context:
            raise MissingRenderContext(missing_context)

        for rename_token in rename_tokens:
            rename = self.render_context[rename_token]

            if not isinstance(rename, str) or len(rename) == 0:
                raise InvalidFolderRename(rename_token)
