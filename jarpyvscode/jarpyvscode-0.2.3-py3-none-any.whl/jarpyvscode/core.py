"""Core functions for the VSCode wrapper and utility tool."""

# Standard library:
import json
import os
import queue
import shutil
import threading
import time
import typing as t
from os.path import abspath
from pathlib import Path
from subprocess import Popen

# 3rd party:
import json5
import psutil

# local:
import jarpyvscode
import jarpyvscode.adaptions
import jarpyvscode.constants as c
import jarpyvscode.environment
import jarpyvscode.insiders
import jarpyvscode.message_and_dialog
import jarpyvscode.paths
import jarpyvscode.usersettings
import jarpyvscode.utils
from jarpyvscode.log import logger


# @logwrap()
def cleanup_for_fast_startup():
    """Clean up to speed up the start of Visual Studio Code."""
    item_names: t.Tuple[str, ...] = (
        # dirs:
        "Backups",
        "Cache",
        "CachedData",
        "CachedExtensions",
        "Code Cache",
        "Crashpad",
        "Dictionaries",
        "GPUCache",
        "Local Storage",
        "Session Storage",
        "blob_storage",
        "logs",
        # files:
        "Cookies",
        "Cookies-journal",
        "CrashpadMetrics-active.pma",
        "Network Persistent State",
        "TransportSecurity",
    )
    item_name: str
    for item_name in item_names:
        item_path: Path = jarpyvscode.paths.code_dir() / item_name
        msg: str = f"Remove '{item_path}' ..."
        if item_path.is_dir():
            logger.debug(msg)
            shutil.rmtree(path=item_path, ignore_errors=True)
        elif item_path.is_file():
            logger.debug(msg)
            item_path.unlink()


def compose_vscode_launch_command(
    code_exe: str, file_path: t.Optional[str] = None
) -> t.List[str]:
    """Compose command to launch VSCode.

    Parameters
    ----------
    code_exe
        .. seealso::

            Refer to the parameter description for :func:`jarpyvscode.core.launch`

    file_path : optional, the default is None
        Optional path to a file to open in VSCode

    Returns
    -------
    t.List[str]
        Command list that will be passed to ``subprocess.Popen``

    """
    code_path: str = ""
    cmd: t.List[str]
    if "windows" in c.PLATFORM_LOWER:
        # windows
        cmd_str: str
        if code_exe:
            cmd_str = code_exe
        elif jarpyvscode.insiders.is_insiders():
            cmd_str = "code-insiders"
        else:
            cmd_str = "code"
        cmd_str = jarpyvscode.paths.path_backslashed(cmd_str)
        cmd = [cmd_str, "--reuse-window"]
    elif any(
        (
            "darwin" in c.PLATFORM_LOWER,
            "macos" in c.PLATFORM_LOWER,
        )
    ):
        # macOS
        if code_exe:
            code_path = code_exe
        elif jarpyvscode.insiders.is_insiders():
            code_path = "/Applications/Visual Studio Code - Insiders.app"
        else:
            code_path = "/Applications/Visual Studio Code.app"
        if code_path.endswith(".app"):
            cmd = ["/usr/local/bin/bash", "-c", f'/usr/bin/open -a "{code_path}"']
        else:
            cmd = ["/usr/local/bin/code"]
    else:
        # Linux:
        if code_exe:
            code_path = code_exe
        elif jarpyvscode.insiders.is_insiders():
            code_path = "code-insiders"
        else:
            code_path = "code"
        cmd = [code_path, "--reuse-window"]

    if file_path is not None:
        file_path = file_path.replace("\\", "/")
        if file_path.startswith("./"):
            file_path = file_path.replace("./", f"{os.getcwd()}/")
        elif "/" not in file_path:
            file_path = f"{os.getcwd()}/{file_path}"
        if any(
            (
                "darwin" in c.PLATFORM_LOWER,
                "macos" in c.PLATFORM_LOWER,
            )
        ):
            cmd[-1] = f'{cmd[-1]} "{file_path}"'
        else:
            cmd += [file_path]

    if any(
        (
            "darwin" in c.PLATFORM_LOWER,
            "macos" in c.PLATFORM_LOWER,
        )
    ):
        cmd += ["--wait"]
    return cmd


def express_psutil_classes_as_str(
    niceclass: t.Any, ioclass: t.Any
) -> t.Tuple[str, str]:
    """Express psutil classes as string.

    Parameters
    ----------
    niceclass
        Nice class (e. g. ``psutil.HIGH_PRIORITY_CLASS``)
    ioclass
        IO class (e. g. ``psutil.IOPRIO_HIGH``)

    Returns
    -------
    t.Tuple[str, str]
        Tuple with classes expressed as string.

    """
    niceclass_str: str = ""
    if niceclass == psutil.HIGH_PRIORITY_CLASS:  # type: ignore
        niceclass_str = "HIGH_PRIORITY_CLASS"
    elif niceclass == psutil.ABOVE_NORMAL_PRIORITY_CLASS:  # type: ignore
        niceclass_str = "ABOVE_NORMAL_PRIORITY_CLASS"
    elif niceclass == psutil.BELOW_NORMAL_PRIORITY_CLASS:  # type: ignore
        niceclass_str = "BELOW_NORMAL_PRIORITY_CLASS"

    ioclass_str: str = ""
    if ioclass == psutil.IOPRIO_HIGH:  # type: ignore
        ioclass_str = "IOPRIO_HIGH"
    elif ioclass == psutil.IOPRIO_NORMAL:  # type: ignore
        ioclass_str = "IOPRIO_NORMAL"
    elif ioclass == psutil.IOPRIO_LOW:  # type: ignore
        ioclass_str = "IOPRIO_LOW"
    elif ioclass == psutil.IOPRIO_VERYLOW:  # type: ignore
        ioclass_str = "IOPRIO_VERYLOW"

    return niceclass_str, ioclass_str


def launch(
    concurrent: bool,
    code_exe: str = "",
    gui: bool = True,
    file_path: t.Optional[str] = None,
) -> None:
    r"""Adapt/ (optionally) launch VSCode dependent on the current environment.

    Open the optionally passed file in VSCode.

    Parameters
    ----------
    concurrent
        If true, concurrent (parallel) code execution will be enabled
    code_exe
        Path to the executable (Linux or Windows)/ application (macOS) for
        Visual Studio Code or Visual Studio Code Insiders. If omitted, if is expected
        that the executable is in the PATH environment of Windows/ Linux computers so
        that the command ``code`` will be available to launch Visual Studio Code and
        the command ``code-insiders`` will be available to launch Visual Studio Code
        Insiders. On a Mac it is assumed that the application can be found in the
        ``Applications`` directory. On Windows computers the exetubale for Visual
        Studio Code may be located at
        ``"%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code"`` respectively at
        ``"%LOCALAPPDATA%\Programs\Microsoft VS Code Insiders\bin\code-insiders"``.
    gui : optional, the default is True
        Controls if the executable of VSCode will be run
    file_path : optional, the default is None
        Path to a file to be opened in VSCode

    """
    patch()
    threading.currentThread().name = "MAIN"

    logger.info(f"Concurrency is set to '{concurrent}'.")
    if "windows" in c.PLATFORM_LOWER:
        is_alive = False
    else:
        is_alive = jarpyvscode.utils.alive(print_to_stdout=False)

    if not is_alive:
        jarpyvscode.adaptions.adapt(concurrent=concurrent)
    if gui:
        if file_path is not None:
            file_path = abspath(file_path)
        run_vscode(code_exe=code_exe, file_path=file_path)


def monitor_and_control_process(
    q: "queue.Queue[t.Any]",
    process_name: str,
    niceclass: int,
    ioclass: int,
    sleep_time: float,
):
    """Monitor process list and raise nice value for specified process.

    Parameters
    ----------
    q
        FIFO queue
    process_name
        Name of the process (e. g. ``git-bash.exe``, ``pylint.exe``)
    niceclass
        Process priority can be one out of ``psutil.<PRIO_NAME>`` with the
        following ``<PRIO_NAME>`` values:

        * ``psutil.HIGH_PRIORITY_CLASS``
        * ``psutil.ABOVE_NORMAL_PRIORITY_CLASS``
        * ``psutil.BELOW_NORMAL_PRIORITY_CLASS``

        The priorities are described at

        `<https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setpriorityclass#parameters>`_.
    ioclass
        Process I/O priority can be one out of ``psutil.<PRIO_NAME>`` with
        the following ``<PRIO_NAME>`` values:

        * ``psutil.IOPRIO_HIGH``
        * ``psutil.IOPRIO_NORMAL``
        * ``psutil.IOPRIO_LOW``
        * ``psutil.IOPRIO_VERYLOW``

        The I/O priorities are described at

        `<https://psutil.readthedocs.io/en/latest/index.html#psutil.Process.ionice>`_.
    sleep_time
        Sleep time for event loop

    """
    logger.info("Process monitor started.")
    while True:
        time.sleep(sleep_time)
        try:
            item = q.get_nowait()
            if item is None:
                logger.info("Stopping thread ...")
                break
        except queue.Empty:
            pass
        modified_no = 0
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=["pid", "name", "nice"])
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                logger.warning(
                    "psutil could not read the attributes dictionary "
                    "for a process out of the complete process list."
                )
            else:
                if all(
                    (
                        process_name.lower() in pinfo["name"].lower(),
                        pinfo["nice"] != niceclass,
                    )
                ):
                    niceclass_str, ioclass_str = express_psutil_classes_as_str(
                        niceclass=niceclass, ioclass=ioclass
                    )
                    modified_no += 1
                    if "windows" in c.PLATFORM_LOWER:
                        try:
                            proc.nice(niceclass)
                            logger.info(
                                f"Set prio {str(modified_no).zfill(2)} to "
                                f'{niceclass_str} for "{pinfo["name"]}" '
                                f'(PID: {pinfo["pid"]})'
                            )
                        except Exception as e:
                            logger.error(
                                f"Setting prio {str(modified_no).zfill(2)} "
                                f"to {niceclass_str} failed: {str(e)}"
                            )

                        try:
                            proc.ionice(ioclass)
                            logger.info(
                                f"Set ionice {str(modified_no).zfill(2)} to "
                                f'{ioclass_str} for "{pinfo["name"]}" '
                                f'(PID: {pinfo["pid"]})'
                            )
                        except Exception as e:
                            logger.error(
                                f"Setting ionice {str(modified_no).zfill(2)} "
                                f"to {ioclass_str} failed: {str(e)}"
                            )
    logger.info("Stopped process monitor.")
    q.task_done()


def patch():
    """Patch different things.

    Fix annoying indentation behaviour of the extension ``lextudio.restructuredtext``.

    """
    lextudio_restructuredtext_dir: t.Optional[Path] = None
    extensions_dir: t.Optional[Path] = None
    dot_vscode_dir_name: str = ".vscode"
    if jarpyvscode.insiders.is_insiders():
        dot_vscode_dir_name += "-insiders"
    extensions_dir = Path.home() / dot_vscode_dir_name / "extensions"
    if not extensions_dir.is_dir():
        logger.debug(f"The extensions directory '{extensions_dir}' does not exist.")
        return
    if extensions_dir is None:
        raise EnvironmentError(
            "Fix core.py:patch function and define path for variable 'extensions_dir'!"
        )
    for lextudio_restructuredtext_dir in extensions_dir.glob(
        "lextudio.restructuredtext*"
    ):
        pass
    lang_cfg_path: t.Optional[Path] = None
    if (
        lextudio_restructuredtext_dir is not None
        and lextudio_restructuredtext_dir.is_dir()
    ):
        lang_cfg_path = lextudio_restructuredtext_dir / "language-configuration.json"
    if lang_cfg_path is not None:
        cfg: t.Dict[str, t.Any] = json5.loads(lang_cfg_path.read_text())
        if "indentationRules" in cfg:
            del cfg["indentationRules"]
            lang_cfg_path.write_text(json.dumps(obj=cfg, sort_keys=False, indent=4))


def prioritise_vscode():
    """Prioritise VSCode processes."""
    app_name: str = "Visual Studio Code"
    if jarpyvscode.insiders.is_insiders():
        app_name += " Insiders"
    logger.info(f"Prioritise {app_name} processes ...")

    pinfo_key_to_use = "name"
    vscode_search_string_lw: str = ""
    prio_str = f"nice value {c.NICE_VALUE}"
    if "windows" in c.PLATFORM_LOWER:
        vscode_search_string_lw = "code.exe"
        prio_str = "ABOVE_NORMAL_PRIORITY_CLASS"
    elif any(
        (
            "darwin" in c.PLATFORM_LOWER,
            "macos" in c.PLATFORM_LOWER,
        )
    ):
        pinfo_key_to_use = "exe"
        if jarpyvscode.insiders.is_insiders():
            vscode_search_string_lw = "visual studio code - insiders.app"
        else:
            vscode_search_string_lw = "visual studio code.app"
    else:
        if jarpyvscode.insiders.is_insiders():
            vscode_search_string_lw = "code-insiders"
        else:
            vscode_search_string_lw = "code"
    modified_no = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["exe", "name", "pid"])
        except (FileNotFoundError, psutil.NoSuchProcess) as e:
            logger.error(str(e))
        else:
            if pinfo[pinfo_key_to_use] is not None and all(
                (
                    vscode_search_string_lw,
                    vscode_search_string_lw in pinfo[pinfo_key_to_use].lower(),
                )
            ):
                modified_no += 1

                logger.info(
                    f"Set prio {str(modified_no).zfill(2)} to {prio_str} "
                    f'for "{pinfo["name"]}" '
                    f'(PID: {pinfo["pid"]})'
                )
                try:
                    proc.nice(c.NICE_VALUE)
                except (psutil.AccessDenied, PermissionError) as e:
                    jarpyvscode.message_and_dialog.error(
                        "Error when trying to increase the priority "
                        f"of a Visual Studio Code process:\n\n{str(e)}"
                    )
                    break
    if not modified_no:
        logger.info(f"Have not increased the priority for any {app_name} process!")


def run_vscode(code_exe: str, file_path: t.Optional[str] = None):
    """Start Visual Studio Code (VSCode) process.

    Parameters
    ----------
    code_exe
        .. seealso::

            Refer to the parameter description for :func:`jarpyvscode.core.launch`

    file_path : optional, the default is None
        Optional path to a file to open in VSCode

    """
    cmd = compose_vscode_launch_command(code_exe=code_exe, file_path=file_path)
    logger.info("Restore UI state for host ...")
    jarpyvscode.adaptions.ui_state()

    logger.info("Prepare separate thread for launch of VSCode ...")
    vscode_thread = threading.Thread(
        target=vscode_runner,
        args=(cmd,),
        name="VSCode Launcher",
        daemon=False,
    )
    if "windows" in c.PLATFORM_LOWER:
        alive = False
    else:
        # Before we start VSCode we check, if it's already running:
        alive = jarpyvscode.utils.alive(print_to_stdout=False)

    logger.info("Launch VSCode in separate thread ...")
    if not alive:
        cleanup_for_fast_startup()
    vscode_thread.start()

    if not alive:
        logger.info(
            "Tune performance for processes which are expected "
            "to get started during VSCode session ..."
        )
        sleep_sec = 8
        logger.info(f"Sleep {sleep_sec}s so that VSCode can start all processes ...")
        time.sleep(sleep_sec)
        prioritise_vscode()

    # At least on macOS (and I expect on Linux too) it is sufficient
    # to increase process priority for VSCode processes only. All external
    # programs run from within a VSCode session seem to inherit the nice value

    if "windows" in c.PLATFORM_LOWER:
        # queues for external process monitors:
        # The tuples contain:
        # Index 0: Queue
        # Index 1: niceclass  (process priority)
        # Index 2: ioclass  (process I/O  priority)
        # Index 3: Sleep time for endless monitoring loop
        #
        # DEFAULT 'Sleep time' SHOULD BE 0.1 !
        #
        process_monitors: t.Dict[
            str, t.Tuple["queue.Queue[t.Any]", int, int, float]
        ] = {
            "bash.exe": (
                # WILL ALSO HIT 'git-bash.exe'
                queue.Queue(),
                psutil.ABOVE_NORMAL_PRIORITY_CLASS,  # type: ignore
                psutil.IOPRIO_NORMAL,  # type: ignore
                0.1,  # sleep time in secs
            ),
            "flake8.exe": (
                queue.Queue(),
                psutil.HIGH_PRIORITY_CLASS,  # type: ignore
                psutil.IOPRIO_HIGH,  # type: ignore
                0.1,  # sleep time in secs
            ),
            "python.exe": (
                queue.Queue(),
                psutil.HIGH_PRIORITY_CLASS,  # type: ignore
                psutil.IOPRIO_HIGH,  # type: ignore
                0.1,  # sleep time in secs
            ),
            "sphinx-build.exe": (
                queue.Queue(),
                psutil.ABOVE_NORMAL_PRIORITY_CLASS,  # type: ignore
                psutil.IOPRIO_HIGH,  # type: ignore
                0.1,  # sleep time in secs
            ),
        }

        # start process monitors:
        process_monitor_threads: t.List[threading.Thread] = []
        thread: threading.Thread
        for proc_name, proc_params in process_monitors.items():
            q = proc_params[0]
            niceclass = proc_params[1]
            ioclass = proc_params[2]
            sleep_time = proc_params[3]
            thread = threading.Thread(
                target=monitor_and_control_process,
                args=(
                    q,
                    proc_name,
                    niceclass,
                    ioclass,
                    sleep_time,
                ),
                name=f"{proc_name} monitor",
                daemon=True,
            )
            process_monitor_threads.append(thread)
            thread.start()

        # Launch VSCode:
        vscode_thread.join()

        # stop process monitors:
        for _, proc_params in process_monitors.items():
            q = proc_params[0]
            q.put(None)

        for thread in process_monitor_threads:
            thread.join()


def vscode_runner(cmd: t.List[str]):
    """Run VSCode in a separate thread.

    Parameters
    ----------
    cmd
        Command list that will be passed to ``subprocess.Popen``

    """
    success = True
    shell: bool = False
    cmd_str = " ".join(cmd) if len(cmd) > 1 else cmd[0]
    try:
        logger.info(f"Execute '{cmd_str}' ...")
        env: t.Dict[str, str] = {"JARROOT": str(jarpyvscode.usersettings.jarroot())}
        if any(
            (
                "darwin" in c.PLATFORM_LOWER,
                "macos" in c.PLATFORM_LOWER,
            )
        ):
            logger.debug(
                "'Execute Popen(cmd, shell=shell, env=env).wait()' "
                f"with: cmd='{cmd}', shell='{shell}', env={env}, "
                f"in cwd='{os.getcwd()}' ..."
            )
            Popen(cmd, shell=shell, env=env).wait()
        else:
            shell = "windows" in c.PLATFORM_LOWER
            logger.debug(
                "'Execute Popen(cmd, shell=shell, env=env).wait()' "
                f"with: cmd='{cmd}', shell='{shell}' "
                f"in cwd='{os.getcwd()}' ..."
            )
            Popen(cmd, shell=shell).wait()
    except BaseException as e:
        success = False
        print("\n\n\n")
        logger.error(f"COMMAND '{cmd_str}' FAILED: '{e}'")
        print("\n\n\n")
    if success:
        jarpyvscode.adaptions.ui_state()
