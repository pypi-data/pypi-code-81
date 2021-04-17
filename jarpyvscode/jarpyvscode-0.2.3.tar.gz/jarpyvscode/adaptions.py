"""Module with functions adapting VSCode to the environment where it's being used.

This includes modifications of multiple configuration databases
and files (e. g. settings.json, .code-workspace files etc.).

"""

# Standard library:
import codecs
import json
import os
import queue
import shutil
import sqlite3
import threading
import typing as t
from collections import OrderedDict
from os.path import abspath, basename, dirname, isfile, join
from pathlib import Path

# local:
import jarpyvscode
import jarpyvscode.constants
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.paths

# import jarpyvscode.setups
import jarpyvscode.utils
from jarpyvscode.log import logger

CONCURRENT: bool
MODULE_DIR = abspath(str(Path(__file__).parents[0]))


def adapt(concurrent: bool, inplace: bool = True) -> None:
    """Adapt setting/ configuration files depending on used computer.

    Human-readable ASCII files and SQLite databases are considered when
    file paths or machine-dependent settings are set.

    Parameters
    ----------
    concurrent
        If true, concurrent (parallel) code execution will be enabled
    inplace : optional, the default is True
        If true, setting/ configuration files are being
        adapted inplace. Otherwise, adapted files will be
        stored besides the original ones whereby the last ``'.'`` in
        the file name will be replaced by ``'_adapted.'``.

    """
    global CONCURRENT
    CONCURRENT = concurrent  # type: ignore
    logger.info("Adapt VSCode configuration ...")
    vsc_config_file_paths = jarpyvscode.utils.collect_vsc_config_file_paths()

    if concurrent:

        def worker(
            q: "queue.Queue[t.Any]",
            func: t.Callable[[bool, t.Optional[t.List[str]], bool], None],
            args: t.Tuple[bool, t.Optional[t.List[str]], bool],
        ):
            try:
                func(*args)
                q.task_done()
            except Exception as e:
                q.task_done()
                raise e

        funcs: t.Tuple[t.Callable[[t.Optional[t.List[str]], bool], None], ...] = (
            adapt_global_workspace_storages,
            adapt_workspace_storages,
        )
        args: t.Tuple[t.Optional[t.List[str]], bool] = (
            vsc_config_file_paths,
            inplace,
        )

        queues: t.List[queue.Queue] = []
        threads: t.List[threading.Thread] = []

        for func in funcs:
            q: "queue.Queue[t.Any]" = queue.Queue()
            queues.append(q)

            threads.append(
                threading.Thread(
                    name=func.__name__,
                    target=worker,
                    args=(q, func, args),
                    daemon=True,
                )
            )

        _ = [q.put(None) for q in queues]  # type: ignore
        _ = [t.start() for t in threads]  # type: ignore
        _ = [q.join() for q in queues]  # type: ignore
        _ = [t.join() for t in threads]  # type: ignore
    else:
        adapt_global_workspace_storages(
            vsc_config_file_paths=vsc_config_file_paths,
            inplace=inplace,
        )
        adapt_workspace_storages(
            vsc_config_file_paths=vsc_config_file_paths,
            inplace=inplace,
        )


def adapt_global_storage_json(file_path: str, inplace: bool = True) -> None:
    """Adapt ``storage.json`` file depending on used computer.

    .. note:: There is only one file named ``storage.json``.

    The file ``storage.json`` is located at ``Code/storage.json``.

    Parameters
    ----------
    file_path
        Path to ``storage.json`` file
    inplace
        If true, ``storage.json`` file is being adapted inplace.
        Otherwise, adapted global workspace storage file will be stored as
        ``storage_adapted.json`` besides the original one for debugging purposes.

    """
    logger.debug("Processing global 'storage.json' ...")

    if not isfile(file_path):
        return
    with codecs.open(file_path, "r", "utf-8") as f:
        json_data = json.load(f)

    # workspaces:
    workspace_items = None
    try:
        workspace_items = json_data["openedPathsList"]["workspaces3"]
    except KeyError:
        logger.error('Cannot find key chain "openedPathsList", "workspaces3"!')
    if workspace_items is not None:
        for workspace_item in workspace_items:
            if isinstance(workspace_item, dict):
                # dict with keys 'id' and 'configURIPath':
                old_path = workspace_item["configURIPath"]
                new_path = jarpyvscode.utils.adapt_jarroot_in_path(old_path=old_path)
                new_path = jarpyvscode.paths.path_remove_drive_letter(new_path)
                workspace_item["configURIPath"] = new_path
            elif isinstance(workspace_item, str):
                # string describing a 'file://' path:
                old_path = workspace_item
                new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                    old_path=old_path, colon_str=r"%3A"
                )
                workspace_item = new_path
    # files:
    old_file_items = None
    try:
        old_file_items = json_data["openedPathsList"]["files2"]
    except KeyError:
        logger.error('Cannot find key chain "openedPathsList", "files2"!')
    if old_file_items is not None:
        new_file_items = []
        for old_file_item in old_file_items:
            new_file_item = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=old_file_item, colon_str=r"%3A"
            )
            new_file_items.append(new_file_item)
        json_data["openedPathsList"]["files2"] = new_file_items
    # last active window:
    last_active_window = None
    try:
        last_active_window = json_data["windowsState"]["lastActiveWindow"]
    except KeyError:
        logger.warning("Cannot find key chain 'windowsState', 'lastActiveWindow'!")
    if last_active_window is not None:
        # workspaceIdentifier:
        workspaceIdentifier = None
        try:
            workspaceIdentifier = last_active_window["workspaceIdentifier"]
        except KeyError:
            logger.debug(
                'Cannot find key chain "windowsState", '
                '"lastActiveWindow", "workspaceIdentifier"!'
            )
        if workspaceIdentifier is not None:
            old_path = workspaceIdentifier["configURIPath"]
            new_path = jarpyvscode.utils.adapt_jarroot_in_path(old_path=old_path)
            new_path = jarpyvscode.paths.path_remove_drive_letter(new_path)
            workspaceIdentifier["configURIPath"] = new_path
            # backupPath:
            workspace_id = workspaceIdentifier["id"]
            code_dir: Path = jarpyvscode.paths.code_dir()
            if not code_dir.is_dir():
                return
            new_backup_path = jarpyvscode.paths.normalise_path(
                join(
                    str(code_dir),
                    "Backups",
                    workspace_id,
                )
            )
            new_backup_path = jarpyvscode.paths.path_backslashed(new_backup_path)
            new_backup_path = jarpyvscode.paths.path_lower_drive_letter(new_backup_path)
            last_active_window["backupPath"] = new_backup_path
    if inplace:
        adapted_file_path = file_path
    else:
        adapted_file_path = file_path.replace(".json", "_adapted.json")

    with codecs.open(adapted_file_path, "w", "utf-8") as f:
        json.dump(json_data, f, indent=4, sort_keys=False)

    logger.debug("Processed global 'storage.json'.")


def adapt_global_workspace_storages(
    vsc_config_file_paths: t.Optional[t.List[str]] = None,
    inplace: bool = True,
) -> None:
    """Adapt global workspace storages depending on used computer.

    Global workspace storage files are stored at

    * ``Code/storage.json``,
    * ``Code/User/globalStorage/state.vscdb``, and
    * ``Code/User/globalStorage/state.vscdb.backup``.

    ``state.vscdb`` and ``state.vscdb.backup`` files are SQLite
    databases.

    Parameters
    ----------
    vsc_config_file_paths :  optional, the default is None
        List of Visual Studio Code setting/ config file paths.
        If None,
        :func:`collect_vsc_config_file_paths()
        <jarpyvscode.collect_vsc_config_file_paths>` will be called to get
        the list of files.
    inplace : optional, the default is True
        If true, global workspace storage files are
        being adapted inplace. Otherwise, adapted global workspace
        storage files will be stored besides the original ones
        whereby the last ``'.'`` in the file name will be replaced
        by ``'_adapted.'``.

    """
    logger.debug("Process global workspace 'storage.json' files ...")
    if vsc_config_file_paths is None:
        vsc_config_file_paths = jarpyvscode.utils.collect_vsc_config_file_paths()
    json_file_paths = [
        p
        for p in vsc_config_file_paths
        if all(
            (
                jarpyvscode.paths.normalise_path(join("Code", "storage.json"))
                in jarpyvscode.paths.normalise_path(p),
                basename(p) == "storage.json",
            )
        )
    ]
    if json_file_paths:
        global_workspace_json_file_path = json_file_paths[0]
        adapt_global_storage_json(
            file_path=global_workspace_json_file_path,
            inplace=inplace,
        )

    # LOOKS AS IF WE DO NOT NEED TO ADAPT THE RECORDS IN THE FILE
    # ${JARROOT}/repos/vscode/appdata/Code/User/globalStorage/state.vscdb

    # sqlite_file_paths = [
    #     p for p in vsc_config_file_paths
    #     if normalise_path(join('Code', 'User', 'globalStorage'))
    #     in normalise_path(p) and
    #     'vscdb' in basename(p)
    # ]

    # if not sqlite_file_paths:
    #     logger.warning(
    #         'Cannot find global workspace storage SQLite database '
    #         'files named "state.vscdb" or "state.vscdb.backup" '
    #         'expected at "Code/User/globalStorage/"!'
    #     )
    # else:
    #     [
    #         adapt_global_workspace_storage_sqlite_db(p, inplace=inplace)
    #         for p in sqlite_file_paths
    #     ]


def adapt_workspace_storage_json(file_path: str, inplace: bool = True) -> None:
    """Adapt ``workspace.json`` files depending on used computer.

    .. note::

        ``workspace.json`` files are stored at
        ``Code/User/workspaceStorage/<HASH_VAL>/workspace.json``.

    Parameters
    ----------
    file_path
        Path to ``workspace.json`` file
    inplace : optional, the default is True
        If true, ``workspace.json`` file is being
        adapted inplace. Otherwise, adapted workspace storage file
        will be stored as ``workspace_adapted.json`` besides the
        original one for debugging purposes.

    """
    logger.debug(f"Processing {file_path} ...")

    with codecs.open(file_path, "r", "utf-8") as f:
        json_data = json.load(f)

    if "configuration" in json_data:
        configuration = json_data["configuration"]
        zip_obj = zip(("fsPath", "external", "path"), ("\\", "/", "/"))
        for (key, sep) in zip_obj:
            if key not in configuration:
                continue
            old_path = configuration[key]
            colon_str = r"%3A" if key == "external" else ":"
            new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=old_path, colon_str=colon_str, sep=sep
            )
            new_path = jarpyvscode.paths.path_remove_drive_letter(new_path)
            configuration[key] = new_path

    if inplace:
        adapted_file_path = file_path
    else:
        adapted_file_path = file_path.replace(".json", "_adapted.json")

    with codecs.open(adapted_file_path, "w", "utf-8") as f:
        json.dump(json_data, f, indent=2, sort_keys=False)

    logger.debug(f"Processed {file_path}.")


def adapt_workspace_storage_sqlite_db(file_path: str, inplace: bool = True) -> None:
    """Adapt ``state.vscdb(.backup)?`` files depending on used computer.

    .. note::

        ``state.vscdb(.backup)?`` files are stored at
        ``Code/User/workspaceStorage/<HASH_VAL>/``.

    Parameters
    ----------
    file_path
        Path to SQLite database file
    inplace
        If true, SQLite database file is being
        adapted inplace. Otherwise, adapted workspace storage file
        will be stored besides the original file whereby the last
        ``'.'`` in the file name will be replaced by ``'_adapted.'``.

    """
    logger.debug(f"Processing {file_path} ...")

    def adapt_alefragnani_bookmarks(old_value: str):
        try:
            old_json_data = json.loads(old_value)
        except json.JSONDecodeError:
            return None
        old_bookmarks = json.loads(old_json_data["bookmarks"])
        new_bookmarks = []
        for old_bookmark in old_bookmarks:
            if "path" not in old_bookmark:
                continue
            #     print(old_bookmark)
            new_bookmark = old_bookmark
            old_path = old_bookmark["path"]
            new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=old_path, sep="\\"
            )
            new_bookmark["path"] = new_path
            new_bookmarks.append(new_bookmark)
        #     print(new_bookmark)

        new_json_data = {"bookmarks": json.dumps(new_bookmarks)}
        new_value = json.dumps(new_json_data, separators=(",", ":"))
        return new_value

    def adapt_codelens_cache2(old_value: str):
        try:
            old_json_data = json.loads(old_value)
        except json.JSONDecodeError:
            return None
        new_json_data = OrderedDict()
        for old_key, value in old_json_data.items():
            new_key = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=old_key, colon_str=r"%3A"
            )
            new_json_data[new_key] = value
        new_value = json.dumps(new_json_data)
        return new_value

    def adapt_history_entries(old_value: str):
        try:
            old_json_data = json.loads(old_value)
        except json.JSONDecodeError:
            return None
        old_history_entries = old_json_data
        new_history_entries = []
        for old_history_entry in old_history_entries:
            new_history_entry = OrderedDict()
            resource_json = None
            try:
                resource_json = old_history_entry["resourceJSON"]
            except KeyError:
                continue
            if "windows" in c.PLATFORM_LOWER:
                resource_json["_sep"] = 1
            elif "_sep" in resource_json:
                del resource_json["_sep"]
            zip_obj = zip(("fsPath", "external", "path"), ("\\", "/", "/"))
            for (key, sep) in zip_obj:
                if key not in resource_json:
                    continue
                old_path = resource_json[key]
                colon_str = r"%3A" if key == "external" else ":"
                new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                    old_path=old_path, colon_str=colon_str, sep=sep
                )
                if key == "fsPath":
                    new_path = jarpyvscode.paths.path_lower_drive_letter(new_path)
                elif key == "external":
                    if (
                        "windows" in c.PLATFORM_LOWER
                        and "file://" in new_path
                        and "file:///" not in new_path
                    ):
                        new_path = new_path.replace("file://", "file:///")
                    new_path = jarpyvscode.paths.path_lower_drive_letter(new_path)
                elif all(
                    (
                        key == "path",
                        not new_path.startswith("/"),
                        not new_path.startswith("Untitled"),
                    )
                ):
                    new_path = f"/{new_path}"
                resource_json[key] = new_path

            new_history_entry["resourceJSON"] = resource_json
            new_history_entries.append(new_history_entry)

        new_value = json.dumps(new_history_entries, separators=(",", ":"))
        return new_value

    def memento_workbench_editors_files_text_file_editor(old_value: str):
        try:
            json_data = json.loads(old_value)
        except json.JSONDecodeError:
            return None
        text_editor_view_states = json_data["textEditorViewState"]
        for text_editor_view_state in text_editor_view_states:
            old_path = text_editor_view_state[0]
            new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                old_path=old_path, colon_str=r"%3A"
            )
            new_path = jarpyvscode.paths.path_lower_drive_letter(new_path)
            if (
                "windows" in c.PLATFORM_LOWER
                and "file://" in new_path
                and "file:///" not in new_path
            ):
                new_path = new_path.replace("file://", "file:///")
            text_editor_view_state[0] = new_path

        json_data["textEditorViewState"] = text_editor_view_states

        new_value = json.dumps(json_data)
        return new_value

    def memento_workbench_parts_editor(old_value: str):
        try:
            json_data = json.loads(old_value)
        except json.JSONDecodeError:
            return None
        root_data_items: t.Optional[t.Iterable] = None
        try:
            root = json_data["editorpart.state"]["serializedGrid"]["root"]
            root_data_items = root["data"]
        except KeyError:
            logger.error(
                "Cannot find key chain "
                '"editorpart.state", "serializedGrid", "root", "data"'
            )
        if root_data_items is not None:
            for root_data_item in root_data_items:
                editors = root_data_item["data"]["editors"]
                for editor in editors:
                    editor_value_json = json.loads(editor["value"])

                    # resource:
                    if "resource" in editor_value_json:
                        old_path = editor_value_json["resource"]
                        if isinstance(editor_value_json["resource"], dict):
                            for key in ("fsPath", "path"):
                                if key in editor_value_json["resource"]:
                                    old_path = editor_value_json["resource"][key]
                                    new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                                        old_path=old_path,
                                        colon_str=r"%3A",
                                    )
                                    new_path = (
                                        jarpyvscode.paths.path_lower_drive_letter(
                                            new_path
                                        )
                                    )
                                    if (
                                        "windows" in c.PLATFORM_LOWER
                                        and "file://" in new_path
                                        and "file:///" not in new_path
                                    ):
                                        new_path = new_path.replace(
                                            "file://", "file:///"
                                        )
                                    editor_value_json["resource"][key] = new_path

                    # resourceJSON:
                    if "resourceJSON" in editor_value_json:
                        if "windows" in c.PLATFORM_LOWER:
                            editor_value_json["resourceJSON"]["_sep"] = 1
                        elif "_sep" in editor_value_json["resourceJSON"]:
                            del editor_value_json["resourceJSON"]["_sep"]

                        old_path = editor_value_json["resourceJSON"]["fsPath"]
                        new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                            old_path=old_path, sep="\\"
                        )
                        new_path = jarpyvscode.paths.path_lower_drive_letter(new_path)
                        editor_value_json["resourceJSON"]["fsPath"] = new_path

                        old_path = editor_value_json["resourceJSON"]["external"]
                        new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                            old_path=old_path, colon_str=r"%3A"
                        )
                        new_path = jarpyvscode.paths.path_lower_drive_letter(new_path)
                        if (
                            "windows" in c.PLATFORM_LOWER
                            and "file://" in new_path
                            and "file:///" not in new_path
                        ):
                            new_path = new_path.replace("file://", "file:///")
                        editor_value_json["resourceJSON"]["external"] = new_path

                        old_path = editor_value_json["resourceJSON"]["path"]
                        new_path = jarpyvscode.utils.adapt_jarroot_in_path(
                            old_path=old_path
                        )
                        if all(
                            (
                                not new_path.startswith("/"),
                                not new_path.startswith("Untitled"),
                            )
                        ):
                            new_path = f"/{new_path}"
                        editor_value_json["resourceJSON"]["path"] = new_path
                    editor["value"] = json.dumps(
                        editor_value_json, separators=(",", ":")
                    )
        new_value = json.dumps(json_data, separators=(",", ":"))
        return new_value

    def workbench_explorer_tree_view_state(old_value: str):
        try:
            json_data = json.loads(old_value)
        except json.JSONDecodeError:
            return None
        for key in ("focus", "selection", "expanded"):
            old_items: t.Optional[t.Iterable] = None
            try:
                old_items = json_data[key]
            except KeyError:
                logger.error("Cannot find key 'expanded'!")
            new_items = []
            if old_items is not None:
                for old_item in old_items:
                    new_item = jarpyvscode.utils.adapt_jarroot_in_path(
                        old_path=old_item, colon_str=r"%3A"
                    )
                    new_item = jarpyvscode.paths.path_lower_drive_letter(new_item)
                    if (
                        "windows" in c.PLATFORM_LOWER
                        and "file://" in new_item
                        and "file:///" not in new_item
                    ):
                        new_item = new_item.replace("file://", "file:///")
                    new_items.append(new_item)
            json_data[key] = new_items
        new_value = json.dumps(json_data)
        return new_value

    if not inplace:
        if "backup" in file_path:
            new_file_path = file_path.replace(".backup", "_adapted.backup")
        else:
            new_file_path = file_path.replace(".vscdb", "_adapted.vscdb")
        if isfile(new_file_path):
            os.remove(new_file_path)
        shutil.copy2(file_path, new_file_path)
        file_path = new_file_path
    try:
        con = sqlite3.connect(file_path)
    except sqlite3.OperationalError as e:
        logger.warning("'{}': {}", file_path, str(e))
        return
    con.row_factory = dict_factory
    cursor = con.cursor()

    records = cursor.execute("SELECT * FROM ItemTable")
    update_dict = {}
    for record in records:
        key = record["key"]
        old_value = record["value"]
        new_value = None
        if key == "alefragnani.Bookmarks":
            new_value = adapt_alefragnani_bookmarks(old_value)
        elif key == "codelens/cache2":
            new_value = adapt_codelens_cache2(old_value)
        elif key == "history.entries":
            new_value = adapt_history_entries(old_value)
        elif key == "memento/workbench.editors.files.textFileEditor":
            new_value = memento_workbench_editors_files_text_file_editor(old_value)
        elif key == "memento/workbench.parts.editor":
            new_value = memento_workbench_parts_editor(old_value)
        elif key == "workbench.explorer.treeViewState":
            new_value = workbench_explorer_tree_view_state(old_value)
        else:
            continue
        if new_value is not None:
            update_dict[key] = new_value

    for key, value in update_dict.items():
        cursor.execute("UPDATE ItemTable SET value=? WHERE key=?", (value, key))
    con.commit()
    con.close()

    logger.debug(f"Processed {file_path}.")


def adapt_workspace_storages(
    vsc_config_file_paths: t.Optional[t.List[str]] = None,
    inplace: bool = True,
):
    """Adapt workspace storages depending on used computer.

    .. note::

        Workspace storage files are stored at

        * ``Code/User/workspaceStorage/<HASH_VAL>/workspace.json``,
        * ``Code/User/workspaceStorage/<HASH_VAL>/state.vscdb``, and
        * ``Code/User/workspaceStorage/<HASH_VAL>/state.vscdb.backup``.

        ``state.vscdb`` and ``state.vscdb.backup`` files are SQLite
        databases.

    Parameters
    ----------
    vsc_config_file_paths : optional, the default is None
        List of Visual Studio Code setting/ config file paths.
        If None,
        :func:`collect_vsc_config_file_paths()
        <jarpyvscode.utils.collect_vsc_config_file_paths>` will be called to get
        the list of files.

    inplace : optional, the default is True
        If true, workspace storage files are being
        adapted inplace. Otherwise, adapted workspace storage files
        will be stored besides the original ones whereby the last
        ``"."`` in the file name will be replaced by
        ``"_adapted."``.

    """
    if vsc_config_file_paths is None:
        vsc_config_file_paths = jarpyvscode.utils.collect_vsc_config_file_paths()

    workspace_json_file_paths = [
        p
        for p in vsc_config_file_paths
        if jarpyvscode.paths.normalise_path(join("Code", "User", "workspaceStorage"))
        in jarpyvscode.paths.normalise_path(p)
        and basename(p) == "workspace.json"
    ]
    sqlite_file_paths = [
        p
        for p in vsc_config_file_paths
        if jarpyvscode.paths.normalise_path(join("Code", "User", "workspaceStorage"))
        in jarpyvscode.paths.normalise_path(p)
        and "vscdb" in basename(p)
        and "backup" not in basename(p)
    ]
    if inplace:
        # concurrent execution during production runtime (inplace=True) only,
        # since it is difficult to debug concurrent programs
        # if jarpyvscode.constants.CONCURRENCY == "multiprocessing":
        #     # json:
        #     with multiprocessing.Pool() as pool:
        #         pool.map(adapt_workspace_storage_json, workspace_json_file_paths)
        #     # sqlite:
        #     with multiprocessing.Pool() as pool:
        #         pool.map(adapt_workspace_storage_sqlite_db, sqlite_file_paths)
        global CONCURRENT
        if CONCURRENT:

            # queues:
            q_json: "queue.Queue[t.Any]" = queue.Queue()
            q_sqlite: "queue.Queue[t.Any]" = queue.Queue()

            # DEFINE WORKERS:

            # json:
            def json_worker():
                while True:
                    # time.sleep(0.01)
                    item = q_json.get()  # block until item received
                    if item is None:
                        break
                    try:
                        adapt_workspace_storage_json(file_path=item)
                        logger.debug(f"Processed '{item}'.")
                        q_json.task_done()
                    except Exception as e:
                        logger.error(str(e))
                        q_json.task_done()

            # sqlite:
            def sqlite_worker():
                while True:
                    # time.sleep(0.01)
                    item = q_sqlite.get()  # block until item received
                    if item is None:
                        break
                    try:
                        adapt_workspace_storage_sqlite_db(file_path=item)
                        logger.debug(f"Processed '{item}'.")
                        q_sqlite.task_done()
                    except Exception as e:
                        logger.error(str(e))
                        q_sqlite.task_done()

            # DEFINE AND START THREADS:
            json_threads, sqlite_threads = [], []
            json_workers_count = len(workspace_json_file_paths)
            sqlite_workers_count = len(sqlite_file_paths)

            # json:
            for item in workspace_json_file_paths:
                t = threading.Thread(target=json_worker, name=basename(item))
                t.start()
                json_threads.append(t)

            # sqlite:
            for item in sqlite_file_paths:
                t = threading.Thread(target=sqlite_worker, name=basename(item))
                t.start()
                sqlite_threads.append(t)

            # FEED THREADS:
            for item in workspace_json_file_paths:
                q_json.put(item)
            for item in sqlite_file_paths:
                q_sqlite.put(item)

            # block until all tasks are done
            q_json.join()
            q_sqlite.join()

            # STOP WORKERS

            # json:
            for _ in range(json_workers_count):
                q_json.put(None)
            for t in json_threads:
                t.join()

            # sqlite:
            for _ in range(sqlite_workers_count):
                q_sqlite.put(None)
            for t in sqlite_threads:
                t.join()

        else:
            for p in workspace_json_file_paths:
                adapt_workspace_storage_json(file_path=p, inplace=inplace)
            for p in sqlite_file_paths:
                adapt_workspace_storage_sqlite_db(file_path=p, inplace=inplace)
    else:
        for p in workspace_json_file_paths:
            adapt_workspace_storage_json(file_path=p, inplace=inplace)
        for p in sqlite_file_paths:
            adapt_workspace_storage_sqlite_db(file_path=p, inplace=inplace)


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> t.Dict[t.Any, t.Any]:
    """Implement a more advanced way for returning SQLite query results.

    .. seealso::

        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory

    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def ui_state() -> None:
    """Restore window position and size for the currently used computer.

    Read machine-dependent value for key chain ``<HOSTNAME>`` > ``uiState`` from
    ``vscode.json`` and replace the value for the key chain
    ``windowsState`` > ``lastActiveWindow`` > ``uiState`` in the file
    ``Code/storage.json`` by the machine-dependent value.

    """
    vscode_json_file_path = jarpyvscode.paths.normalise_path(
        join(MODULE_DIR, "vscode.json")
    )
    if not isfile(vscode_json_file_path):
        logger.warning(f"Cannot find the file '{vscode_json_file_path}'!")
        return
    code_dir: Path = jarpyvscode.paths.code_dir()
    if not code_dir.is_dir():
        return
    storage_json_file_path = jarpyvscode.paths.normalise_path(
        join(
            str(code_dir),
            "storage.json",
        )
    )
    if not isfile(storage_json_file_path):
        logger.warning(f"Cannot find the file '{storage_json_file_path}'!")
        return
    with codecs.open(vscode_json_file_path, "r", "utf-8") as f:
        vscode_json_data = json.load(f)
    if c.HOSTNAME not in vscode_json_data:
        return
    if "uiState" not in vscode_json_data[c.HOSTNAME]:
        return
    _ui_state = vscode_json_data[c.HOSTNAME]["uiState"]

    with codecs.open(storage_json_file_path, "r", "utf-8") as f:
        storage_json_data = json.load(f)
    if "windowsState" not in storage_json_data:
        return
    if "lastActiveWindow" not in storage_json_data["windowsState"]:
        return
    if "uiState" not in storage_json_data["windowsState"]["lastActiveWindow"]:
        return
    windowsState = storage_json_data["windowsState"]
    windowsState["lastActiveWindow"]["uiState"] = _ui_state
    with codecs.open(storage_json_file_path, "w", "utf-8") as f:
        json.dump(storage_json_data, f, indent=4)
