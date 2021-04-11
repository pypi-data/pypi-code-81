import os
from pathlib import Path
from shutil import copyfile, move, rmtree

from simple_pipes import pipe_call
from walkmate import get_child_files

from templ8.models.collection import Collection
from templ8.models.reporter import Reporter
from templ8.models.state import State
from templ8.services.jinja import parse_template
from templ8.utils.paths import (
    create_parents,
    replace_head,
    replace_tail,
    trim_tail,
)


def generate(
    dry_run: bool,
    output_dir: str,
    state: State,
    reporter: Reporter,
) -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if state.inputs.clear_top_level:
        reporter.show_clear_top_level()

        pre_clear_top_level(
            dry_run,
            output_dir,
            state,
            reporter,
        )

    for collection in state.collections:
        reporter.show_collection(collection)

        write_files(
            dry_run,
            output_dir,
            state,
            collection,
            reporter,
        )

        rename_folders(
            dry_run,
            output_dir,
            state,
            collection,
            reporter,
        )

        run_initialization(
            dry_run,
            output_dir,
            collection,
            reporter,
        )


def pre_clear_top_level(
    dry_run: bool,
    output_dir: str,
    state: State,
    reporter: Reporter,
) -> None:
    for filename in os.listdir(output_dir):
        path = os.path.join(output_dir, filename)

        if os.path.isfile(path):

            if filename in state.protected:
                reporter.show_protect_file(filename)

            else:
                reporter.show_delete_file(filename)

                if not dry_run:
                    os.remove(path)


def write_files(
    dry_run: bool,
    output_dir: str,
    state: State,
    collection: Collection,
    reporter: Reporter,
) -> None:
    for template in collection.templates:
        output_path = os.path.join(output_dir, template.output_path)

        if (
            template.output_path in state.protected
            and os.path.exists(output_path)
        ):
            reporter.show_protect_file(template.output_path)

        else:
            reporter.show_write_template(template)

            if not dry_run:
                create_parents(output_path)

                parse_template(
                    os.path.join(collection.path, template.path),
                    output_path,
                    state.render_context,
                    state.inputs.loader_paths,
                )

    for static_file in collection.static_files:
        output_path = os.path.join(output_dir, static_file)

        if static_file in state.protected and os.path.exists(
            output_path
        ):
            reporter.show_protect_file(static_file)

        else:
            reporter.show_write_static_file(static_file)

            if not dry_run:
                create_parents(output_path)

                copyfile(
                    os.path.join(collection.path, static_file),
                    output_path,
                )


def rename_folders(
    dry_run: bool,
    output_dir: str,
    state: State,
    collection: Collection,
    reporter: Reporter,
) -> None:
    for (
        folder,
        rename_token,
    ) in collection.dynamic_folders.items():
        rename = replace_head(
            folder, state.render_context[rename_token]
        )
        reporter.show_rename_folder(folder, rename)

        # Use normpath to match the unix path definitions in
        # metadata.json to the current platform's os.
        source_dir = os.path.normpath(
            os.path.join(output_dir, folder)
        )
        target_dir = os.path.normpath(
            os.path.join(output_dir, rename)
        )

        for long_source in get_child_files(source_dir):
            long_target = replace_tail(
                long_source, source_dir, target_dir
            )

            source = trim_tail(long_source, output_dir)
            target = trim_tail(long_target, output_dir)

            if target in state.protected:
                reporter.show_protect_file(target)

            elif not dry_run:
                create_parents(long_target)
                reporter.show_move_file(source, target)
                move(long_source, long_target)

        if os.path.exists(source_dir) and source_dir != target_dir:
            rmtree(source_dir)


def run_initialization(
    dry_run: bool,
    output_dir: str,
    collection: Collection,
    reporter: Reporter,
) -> None:
    for cmd in collection.initialization:
        reporter.show_run_initialization(cmd)

        if not dry_run:
            pipe_call(cmd.split(" "), cwd=output_dir)
