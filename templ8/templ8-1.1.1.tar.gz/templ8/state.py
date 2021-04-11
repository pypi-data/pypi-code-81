from typing import Any, Dict, List, Tuple

from .models.collection import Collection
from .models.inputs import Inputs
from .services.dynamic import dynamic_render_context
from .services.jinja import combine_schemas
from .utils.dicts import merge_dicts


def load_state(
    input_file: str,
) -> Tuple[Inputs, List[Collection], Dict[str, Any], Dict[str, Any]]:
    inputs = Inputs.from_file(input_file)

    collections = Collection.gather(
        inputs.collections, inputs.includes, inputs.collection_sources
    )

    schema = merge_dicts(
        {"required": []}, combine_schemas(collections)
    )

    render_context = merge_dicts(
        dynamic_render_context,
        *[collection.default_variables for collection in collections],
        inputs.render_context,
    )

    return inputs, collections, schema, render_context
