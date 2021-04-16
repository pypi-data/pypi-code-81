from typing import Dict

from threedi_settings.mappings import swagger_definitions_map, swagger_url_map
from threedi_settings.http.helpers import (
    get_threedi_openapi_specification, SwaggerSpecificationCode
)
try:
    import yaml
    import typer
    from rich.console import Console
    from rich.tree import Tree
    from rich.panel import Panel
except ImportError:
    raise ImportError(
        "You need to install the extra 'cmd', e.g. pip install threedi-settings[cmd]"  # noqa
    )

helper_app = typer.Typer()

SETTINGS_FIELD_STYLES = {
    'description': "[bold cyan]",
    'type': "[italic gold1]",
    'maximum': "[italic orange3]",
    'minimum': "[italic dark_goldenrod]"
}

console = Console()


def set_attrs(field_def: Dict, tree: Tree) -> None:
    """
    adds the field definitions that match the keys in
    SETTINGS_FIELD_STYLES to the given tree instance
    """

    for field, style in SETTINGS_FIELD_STYLES.items():
        value = field_def.get(field, "")
        if not value:
            continue
        value_str = f"{style}{value}"
        tree_str = f"{field}: {value_str}"
        tree.add(tree_str)


@helper_app.command()
def settings_description():
    """
    Shows all API V3 simulation settings fields, help texts on how to use them,
    suitable defaults, types etc.
    """
    tree = Tree("Settings Description")

    code, resp = get_threedi_openapi_specification()
    if code != SwaggerSpecificationCode.ok:
        console.print(f"[red] Error: {resp}")
        raise typer.Exit(code)
    content = yaml.load_all(resp, Loader=yaml.FullLoader)

    swagger_defs = next(content)["definitions"]
    for swagger_key, map in swagger_definitions_map.items():
        url = swagger_url_map[swagger_key]
        p = Panel(
            f":wrench: {swagger_key}",
            style="bold green",
            border_style="green",
            title=url
        )
        sub_tree = tree.add(p)
        for field_name, info in map.items():
            try:
                field_def = swagger_defs[swagger_key]["properties"][field_name]
                field_tree = sub_tree.add(f"[green]{field_name}")
                set_attrs(field_def, field_tree)
            except KeyError as err:
                print(f"{err} {field_name}")
                pass
    console.print(tree)


if __name__ == "__main__":
    helper_app()
