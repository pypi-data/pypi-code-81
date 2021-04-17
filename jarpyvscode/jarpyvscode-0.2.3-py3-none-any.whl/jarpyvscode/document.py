"""Module with tools to deal with a document in VSCode."""

# Standard library:
import json
import re
import typing as t
from operator import itemgetter
from pathlib import Path

# 3rd party:
import json5

# local:
from jarpyvscode.log import logger


def filter_lines(
    file_path: Path, filter_value: str, filter_type: str, case_sensitive: bool, eol: int
):
    r"""Filter lines of a document given in a file.

    Parameters
    ----------
    file_path
        Path to the file containing a document to be filtered

    filter_value
        The value of the filter

    filter_type
        Can be ``"string"`` or ``"regex"``

    case_sensitive
        If true and *filter_type* is set to ``"string"``, a case-sensitive filter will
        be applied

    eol
        End of line string. Can be 1 for ``"\n"`` or 2 for ``"\r\n"``

    """
    if not file_path.is_file():
        logger.error(f'Cannot find the temporary file "{file_path}" to be formatted!')
        return
    logger.info(f"Filter value: '{filter_value}'")
    logger.info(f"Filter type: '{filter_type}'")
    if filter_type == "string":
        logger.info(f"case-sensitive: {case_sensitive}")
    content: str = file_path.read_text()
    end_of_line: str = "\n" if eol == 1 else "\r\n"
    lines: t.List[str]
    if end_of_line in content:
        lines = content.split(end_of_line)
    else:
        lines = [content]
    logger.info(f"Document to analyse has {len(lines)} line(s).")
    filtered_lines: t.List[str] = []
    if filter_type == "string":
        if case_sensitive:
            filtered_lines = [line for line in lines if filter_value in line]
        else:
            filtered_lines = [
                line for line in lines if filter_value.lower() in line.lower()
            ]
    elif filter_type == "regex":
        filtered_lines = [
            line for line in lines if re.match(filter_value, line) is not None
        ]
    logger.info(f"Filtered {len(filtered_lines)} line(s).")
    file_path.write_text(end_of_line.join(filtered_lines))


def format_document(
    temp_file_path: Path,
    language_id: str,
    insert_spaces: bool,
    tab_size: int,
    sort_keys: bool = False,
    file_path: t.Optional[Path] = None,
):
    r"""Format document given in a file.

    Parameters
    ----------
    temp_file_path
        Path to a temporary file containing a document to be formatted. The file is a
        temporary file because it can be, that the user wants to format the content of
        a buffer in VSCode that has not been stored on the disk so far.

    language_id
        VSCode language id. Currently understood ids:

        * ``json``
        * ``jsonc``

    insert_spaces
        If true, indent with *tab_size* spaces. Otherwise, indent with ``"\t"``

    tab_size
        Considered, if *insert_spaces* is true. Equals indent level for pretty printing.

    sort_keys
        If true, keys in the JSON data will be sorted. Considered, when *language_id*
        is one out of ``"json"`` or ``"jsonc"``.

    file_path
        Absolute path to the file to be formatted. This can be None because it can be,
        that the user wants to format the content of a buffer in VSCode that has not
        been stored on the disk so far.
        If a file path is given, it can be used to fine-tune how the formatting will
        look like (e. g. sort a list of dictionaries in a JSON file by specific
        dictionary keys for ``assets.json``).

    """
    logger.info(f"temp_file_path: '{temp_file_path}'")
    logger.info(f"language_id: '{language_id}'")
    logger.info(f"insert_spaces: {insert_spaces}")
    logger.info(f"tab_size: {tab_size}")
    logger.info(f"sort_keys: {sort_keys}")
    logger.info(f"file_path: '{file_path}'")
    if file_path is not None and any(
        (
            str(file_path).endswith(".vscode-insiders/argv.json"),
            str(file_path).endswith(".vscode/argv.json"),
            str(file_path).endswith("finances/data/financial_positions.jsonc"),
        )
    ):
        logger.info(f"Ignoring file '{file_path}.'")
        return
    if temp_file_path.is_file():
        logger.info(f"Read content from '{temp_file_path}' ...")
        file_content: str = temp_file_path.read_text()
        temp_file_path.unlink()
    else:
        logger.error(
            f"Cannot find the temporary file '{temp_file_path}' to be formatted!"
        )
        return
    data: t.Optional[t.Any] = None
    if language_id == "jsonc":
        logger.info("Parse commented JSON content ...")
        data = json5.loads(file_content)
    elif language_id == "json":
        try:
            logger.info("Parse JSON content ...")
            data = json.loads(file_content)
        except json.decoder.JSONDecodeError as e:
            logger.error(
                "Cannot parse JSON file at "
                f"'{temp_file_path if file_path is None else file_path}': '{e}'"
            )

    if language_id.startswith("json") and data is not None:
        indent: t.Union[int, str] = tab_size if insert_spaces else "\t"

        if file_path is not None:
            logger.info("Try to identify kind of file ...")
            if all(
                (
                    "globalStorage/jamilraichouni" in str(file_path),
                    "assets.json" in str(file_path),
                )
            ):
                # assets.json
                logger.info(
                    "Identified Visual Studio Code assets file. "
                    "Will sort assets by keys 'type' and 'title'."
                )
                data = sorted(data, key=itemgetter("type", "title"), reverse=False)
            elif "jamilraichouni.jarpyvscode/host_settings.json" in str(file_path):
                # host_settings.json
                logger.info(
                    "Identified host-specific Visual Studio Code settings. "
                    "Will sort settings by key 'key'."
                )
                data = sorted(data, key=itemgetter("key"))
            elif "User/keybindings.json" in str(file_path):
                # host_settings.json
                logger.info(
                    "Identified Visual Studio Code keybindings. "
                    "Will sort keys and keybindings by keys 'command' and 'key'."
                )
                sort_keys = True
                data = sorted(
                    data,
                    key=itemgetter(
                        "command",
                        "key",
                    ),
                )
            elif (
                re.match(
                    r".*?User.*?snippets.*?\.(json[c]?|code\-snippets)?$",
                    str(file_path),
                )
                is not None
            ):
                # Visual Studio Code snippet files:
                logger.info(
                    "Identified Visual Studio Code snippets file. Will sort keys."
                )
                sort_keys = True
            elif (
                re.match(
                    r".*?(Code.*?User|\.vscode).*?settings\.json$",
                    str(file_path),
                )
                is not None
            ):
                # Visual Studio Code settings.json:
                logger.info(
                    "Identified Visual Studio Code settings file. Will sort keys."
                )
                sort_keys = True

        logger.info(
            f"Write formatted document back to temporary file '{temp_file_path}' ..."
        )
        temp_file_path.write_text(
            data=json.dumps(data, sort_keys=sort_keys, indent=indent) + "\n",
            encoding="utf8",
        )
