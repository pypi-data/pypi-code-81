"""Command line interface for the Python backend of JAR's pyVSCode .

Launch/ prioritise VSCode on different computers or adapt workspaces depending on the
development environment and more.

Some information where VSCode stores what:

**Last opened workspace(s):**

``Code/storage.json``
(see key chain 'openedPathsList' -> 'workspaces3')

**Last opened file(s) when a workspace was loaded:**

``Code/User/workspaceStorage/<HASH_VAL>/state.vscdb``
(see key 'history.entries')

**Last opened file(s) when no workspace was loaded:**

``Code/storage.json``
(see key chain 'openedPathsList' -> 'files2')

"""

# Standard library:
import os
import sys
import typing as t
from pathlib import Path

# 3rd party:
import click

# local:
import jarpyvscode
import jarpyvscode.assets
import jarpyvscode.cli_utils
import jarpyvscode.constants as c
import jarpyvscode.core
import jarpyvscode.document
import jarpyvscode.insiders
import jarpyvscode.project
import jarpyvscode.usersettings
import jarpyvscode.utils
import jarpyvscode.workspace
from jarpyvscode.log import get_log_level_from_cli, logger, logwrap

# constants:
MODULE_DIR: Path = Path(__file__).parents[0]


@click.group()
@click.option(
    "--insiders/--no-insiders",
    is_flag=True,
    default=False,
    show_default=True,
    help="Flag to control kind (insiders or stable build) of Visual Studio Code build.",
)
@click.option("-v", "--verbose", count=True)
@click.option(
    "--debug/--no-debug",
    default=False,
    envvar="VSCODE_DEBUG",
    show_default=True,
    help="Print debug level log messages",
)
@click.pass_context
@logwrap()
def cli(
    ctx: click.Context, insiders: bool = False, verbose: int = 0, debug: bool = False
) -> None:
    """Command line interface for VSCode."""
    logger.remove()
    ctx.obj["CONCURRENT"] = not debug
    os.environ["IS_INSIDERS"] = "1" if insiders else "0"
    ctx.obj["INSIDERS"] = insiders
    level: str = get_log_level_from_cli(debug=debug, verbose=verbose)
    if not c.LOG_DIR.is_dir():
        c.LOG_DIR.mkdir()
    log_file_path: Path = c.LOG_DIR / f"{ctx.invoked_subcommand}.log"
    debug_log_file_path: Path = c.LOG_DIR / f"{ctx.invoked_subcommand}_debug.log"
    logger.add(sys.stderr, level=level)
    try:
        logger.add(str(log_file_path), level="INFO")
        logger.info(f"Logging to '{log_file_path}' with level 'INFO' ...")
        logger.add(str(debug_log_file_path), level="DEBUG")
        logger.info(f"Logging to '{debug_log_file_path}' with level 'DEBUG' ...")
    except PermissionError as e:
        logger.warning(str(e))
    logger.notice(
        f"CLI: {c.PROJECT_NAME} {jarpyvscode.__version__} invoked "
        f"sub command: '{ctx.invoked_subcommand}' with console log level '{level}'."
    )


@cli.command(help=str(jarpyvscode.utils.alive.__doc__).split("\n")[0])
@logwrap()
def alive():
    """Call :func:`jarpyvscode.utils.alive`."""
    jarpyvscode.utils.alive()


@cli.command(
    help=(
        str(jarpyvscode.project.create.__doc__).split("\n")[0] + " "
        "PATH describes a relative or absolute path. If PATH is a relative path, "
        "it will be tried to set it relative to the path $JARROOT/repos. "
        "If $JARROOT is not defined, the path will be set relative to the $HOME "
        "directory."
    )
)
@click.argument("path", default=None, required=True, type=str)
@click.argument("kind", default=None, required=True, type=str)
@logwrap()
def create_project(path: str, kind: str):
    """Call :func:`jarpyvscode.project.create`."""
    jarpyvscode.project.create(name_or_path=path, template_kind=kind)


@cli.command(help=str(jarpyvscode.document.filter_lines.__doc__).split("\n")[0])
@click.argument("file_path", default=None, required=True, type=str)
@click.argument("filter_value", default=None, required=True, type=str)
@click.option(
    "--filter-type",
    default=None,
    required=True,
    help='Type ("string" or "regex") of filter',
)
@click.option(
    "--case-sensitive/--no-case-sensitive",
    default=True,
    is_flag=True,
    help=(
        'If true and filter_type is set to "string", '
        "a case-sensitive filter will be applied"
    ),
)
@click.option(
    "--eol",
    default=None,
    required=True,
    help='Type (1 for "\n" or 2 for "\r\n") of end of line',
    type=int,
)
@logwrap()
def filter_lines(
    file_path: Path, filter_value: str, filter_type: str, case_sensitive: bool, eol: int
):
    """Call :func:`jarpyvscode.document.filter_lines`."""
    jarpyvscode.document.filter_lines(
        Path(file_path), filter_value, filter_type, case_sensitive, eol
    )


@cli.command(help=str(jarpyvscode.document.format_document.__doc__).split("\n")[0])
@click.argument("temp_file_path", default=None, required=True)
@click.option(
    "--language-id",
    default=None,
    required=True,
    help="VSCode language id. Currently understood ids: json, jsonc",
)
@click.option(
    "--insert-spaces/--no-insert-spaces",
    default=True,
    is_flag=True,
    help="If specified, spaces will be used to indent",
)
@click.option(
    "--tab-size",
    default=4,
    help="Number of spaces (defaults to 4), if --insert-spaces is specified",
)
@click.option(
    "--sort-keys/--no-sort-keys",
    default=False,
    required=False,
    is_flag=True,
    help=(
        'If specified and "json" or "jsonc" are passed via --language-id, '
        "keys in the JSON data will be sorted"
    ),
)
@click.option(
    "--file-path",
    default=None,
    required=False,
)
@logwrap()
def format_document(
    temp_file_path: str,
    language_id: str,
    insert_spaces: bool,
    tab_size: int,
    sort_keys: bool = False,
    file_path: t.Optional[str] = None,
):
    """Call :func:`jarpyvscode.document.format_document`."""
    jarpyvscode.document.format_document(
        Path(temp_file_path),
        language_id,
        insert_spaces,
        tab_size,
        sort_keys,
        Path(str(file_path)),
    )


@cli.command(help=str(jarpyvscode.core.launch.__doc__).split("\n")[0])
@click.option(
    "--code-exe",
    is_flag=False,
    help=(
        "Path to the executable (Linux or Windows)/ application (macOS) for "
        "Visual Studio Code or Visual Studio Code Insiders. If omitted, if is expected "
        "that the executable is in the PATH environment of Windows/ Linux computers so "
        "that the command 'code' will be available to launch Visual Studio Code and "
        "the command 'code-insiders' will be available to launch Visual Studio Code "
        "Insiders. On a Mac it is assumed that the application can be found in the "
        "'Applications' directory. On Windows computers the exetubale for Visual "
        "Studio Code may be located at "
        r"'%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code' respectively at "
        r"'%LOCALAPPDATA%\Programs\Microsoft VS Code Insiders\bin\code-insiders'."
    ),
)
@click.option(
    "--gui/--no-gui",
    is_flag=True,
    default=True,
    show_default=True,
    help=(
        "Flag to control if VSCode will be launched or not. "
        "If the flag --no-gui is passed, one can simulate all "
        "preparation steps (adapting workspace files etc.) without finally "
        "launching VSCode."
    ),
)
@click.argument(
    "file",
    default=None,
    required=False,
    callback=jarpyvscode.cli_utils.check_if_file_exists,  # type: ignore
)
@click.pass_context
@logwrap()
def launch(
    ctx: click.Context,
    code_exe: str = "",
    gui: bool = True,
    file: t.Optional[str] = None,
) -> None:
    """Call :func:`jarpyvscode.core.launch` with the specified arguments."""
    jarpyvscode.usersettings.setup()
    jarpyvscode.core.launch(
        concurrent=ctx.obj["CONCURRENT"],
        code_exe=code_exe,
        gui=gui,
        file_path=file,
    )


@cli.command()
@logwrap()
def list_project_kinds():
    """List project kinds that can be passed to :func:`jarpyvscode.project.create`."""
    _ = [print(p) for p in sorted(c.PROJECT_KINDS)]


@cli.command(
    help="""Read the INPUT file (assets.json) of the VSCode extension
'jamilraichouni.jarpyvscode'
and populate any '${MAJOR}', '${MINOR}', and '${PATCH}' placeholders. Write the
populated file to the path defined as OUTPUT.
The Python package versions installed into the conda environment
for the interpreter 'PYTHON_INTERPRETER' will be used to try to populate the
placeholders for cases where a key 'pkg_name' is specified for an asset entry in the
INPUT file.
"""
)
@click.argument("PYTHON_INTERPRETER")
@click.argument("INPUT")
@click.argument("OUTPUT")
@logwrap()
def setup_assets(**kwargs: str) -> None:
    """Call :func:`jarpyvscode.assets.setup` with the specified arguments."""
    jarpyvscode.assets.setup(**kwargs)


@cli.command(help=str(jarpyvscode.project.setup.__doc__).split("\n")[0])
@click.argument("path", default=None, required=True, type=str)
@logwrap()
def setup_project(path: str):
    """Call :func:`jarpyvscode.project.setup`."""
    jarpyvscode.project.setup(project_path=Path(path))


@cli.command(help=str(jarpyvscode.usersettings.setup).__doc__)
@logwrap()
def setup_user_settings() -> None:
    """Call :func:`jarpyvscode.usersettings.setup`."""
    jarpyvscode.usersettings.setup()


@cli.command(help=str(jarpyvscode.workspace.setup.__doc__).split("\n")[0])
@click.argument("code_workspace_file_path")
@logwrap()
def setup_workspace(code_workspace_file_path: str):
    """Call :func:`jarpyvscode.workspace.setup` with the specified argument."""
    jarpyvscode.usersettings.setup()
    try:
        jarpyvscode.workspace.setup(
            code_workspace_file_path=Path(code_workspace_file_path),
        )
    except FileNotFoundError:
        if logger is not None:
            logger.error(
                'Expected a ".code-workspace" file but received '
                f'"{code_workspace_file_path}"!'
            )


if __name__ == "__main__":
    cli(obj={})
    sys.exit(0)
