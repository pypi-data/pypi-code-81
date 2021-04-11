from dataclasses import dataclass
from pprint import pprint
from typing import Any, Dict, List, Set

from art import text2art
from simple_chalk import chalk

from templ8.models.collection import Collection
from templ8.models.inputs import Inputs
from templ8.models.template import Template
from templ8.utils.paths import path_head


@dataclass
class Reporter:
    verbose: bool = False
    schema: bool = False
    silent: bool = False

    title: str = text2art("Templ8", font="ghost")

    def report(self, msg: Any, pretty: bool = False) -> None:
        if not self.silent:
            if pretty:
                pprint(msg)
            else:
                print(msg)

    def show_state(
        self,
        inputs: Inputs,
        collections: List[Collection],
        render_context: Dict[str, Any],
        required_context: Set[str],
    ) -> None:
        if self.verbose:
            for (title, data) in [
                ("Inputs", inputs.__dict__),
                ("Collections", collections),
                ("Required render context", required_context),
                ("Render context", render_context),
            ]:
                self.report("\n" + chalk.green(title))
                self.report(data, pretty=True)

    def show_schema(self, schema: Dict[str, Any]) -> None:
        if self.schema:
            self.report("\n" + chalk.green("Schema"))
            self.report(schema, pretty=True)

    def show_collection(self, collection: Collection) -> None:
        self.report(
            "\n"
            + chalk.green(
                f"Generating {path_head(collection.path)} collection"
            ),
        )

        for (field, count) in [
            ("Templates", len(collection.templates)),
            ("Static files", len(collection.static_files)),
            ("Dynamic folders", len(collection.dynamic_folders)),
            (
                "Initialization scripts",
                len(collection.initialization),
            ),
        ]:
            self.report(f"{field}: {count}")

    def show_clear_top_level(self) -> None:
        self.report(chalk.green("Clearing top level files"))

    def show_protect_file(self, file: str) -> None:
        self.report(chalk.gray("> " + f"Leaving {file} unchanged"))

    def show_write_template(self, template: Template) -> None:
        self.report(
            chalk.blue("> " + f"Templating {template.output_path}")
        )

    def show_write_static_file(self, static_file: str) -> None:
        self.report(chalk.magenta("> " + f"Copying {static_file}"))

    def show_delete_file(self, file: str) -> None:
        self.report(chalk.red("> " + f"Deleting {file}"))

    def show_rename_folder(self, folder: str, rename: str) -> None:
        self.report(
            chalk.cyan("> " + f"Renaming {folder} to {rename}")
        )

    def show_move_file(self, source: str, target: str) -> None:
        self.report(
            chalk.magenta("> " + f"Moving {source} to {target}")
        )

    def show_run_initialization(self, cmd: str) -> None:
        self.report(chalk.yellow("> " + f"Running {cmd}"))
