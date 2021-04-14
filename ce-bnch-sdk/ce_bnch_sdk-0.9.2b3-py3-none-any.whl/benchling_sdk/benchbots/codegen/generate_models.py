from typing import Dict, Union

import black
from jinja2 import Environment, PackageLoader

from benchling_sdk.benchbots.types.manifest import DropdownDependency, Manifest, SchemaDependency


def generate_model(dependency: Union[SchemaDependency, DropdownDependency]) -> str:
    env = Environment(
        loader=PackageLoader("benchling_sdk.benchbots.codegen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    if isinstance(dependency, SchemaDependency):
        template = env.get_template("schema_instance_model.py.jinja2")
    else:
        template = env.get_template("dropdown_model.py.jinja2")

    return black.format_str(template.render(dependency=dependency), mode=black.Mode(line_length=110))


def generate_models(manifest: Manifest) -> Dict[str, str]:
    assert manifest.dependencies
    return {
        dependency.snake_case_name: generate_model(dependency)
        for dependency in manifest.dependencies
        if isinstance(dependency, SchemaDependency)
        and dependency.fieldDefinitions
        or isinstance(dependency, DropdownDependency)
    }
