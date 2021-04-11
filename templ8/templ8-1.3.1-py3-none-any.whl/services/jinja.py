import os
import re
from functools import reduce
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2schema import infer, to_json_schema

from templ8.services.translate import kebab_to_snake, lifecycle_stage
from templ8.utils.dicts import deep_merge_dicts, merge_dicts
from templ8.utils.paths import path_head, path_tail
from templ8.utils.strings import handle, quote

custom_filters = {
    "kebab_to_snake": kebab_to_snake,
    "pad_in": lambda x, n: "".join([" "] * n) + x,
    "to_handle": handle,
    "to_lifecycle_stage": lifecycle_stage,
    "to_quote": quote,
    "without_ends": lambda x: x[1:-1],
    "without_first": lambda x: x[1:],
    "without_last": lambda x: x[:-1],
}


def parse_template(
    template_path: str,
    output_path: str,
    context: Dict[str, Any],
    loader_paths: List[str],
) -> None:
    """
    Parse a jinja template.

    Args:
        template_path (str): Jinja template path.
        output_path (str): Path for parsed template output.
        context (Dict[str, Any]): Render context variables.
    """
    loader_paths.extend([path_tail(template_path), os.getcwd()])

    env = Environment(
        loader=FileSystemLoader(loader_paths),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )

    env.filters = merge_dicts(env.filters, custom_filters)

    with open(output_path, "w") as stream:
        stream.write(
            env.get_template(path_head(template_path)).render(
                **context
            )
        )


def template_schema(path: str) -> Dict[str, Any]:
    custom_tokens = [r"{% include .* %}"]
    custom_tokens.extend(
        [rf"(\| ?)?{i}(\(.*\))?" for i in custom_filters],
    )

    with open(path, "r") as stream:
        return to_json_schema(
            infer(
                reduce(
                    lambda acc, x: re.sub(x, "", acc),
                    custom_tokens,
                    stream.read(),
                )
            )
        )


def combine_schemas(objs: List[Any]) -> Dict[str, Any]:
    return deep_merge_dicts(*[obj.schema for obj in objs])
