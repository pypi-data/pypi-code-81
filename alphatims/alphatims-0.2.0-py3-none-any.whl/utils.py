#!python
"""This module provides generic utilities.
These utilities primarily focus on:

    - logging
    - compilation
    - parallelization
    - generic io
"""

# builtin
import logging
import os
import sys
import json
import contextlib
# local
import alphatims


BASE_PATH = os.path.dirname(__file__)
EXT_PATH = os.path.join(BASE_PATH, "ext")
IMG_PATH = os.path.join(BASE_PATH, "img")
LIB_PATH = os.path.join(BASE_PATH, "lib")
LOG_PATH = os.path.join(BASE_PATH, "logs")
DOC_PATH = os.path.join(BASE_PATH, "docs")
with open(os.path.join(LIB_PATH, "interface_parameters.json"), "r") as in_file:
    INTERFACE_PARAMETERS = json.load(in_file)
MAX_THREADS = INTERFACE_PARAMETERS["threads"]["default"]
PROGRESS_CALLBACK_STYLE_NONE = 0
PROGRESS_CALLBACK_STYLE_TEXT = 1
PROGRESS_CALLBACK_STYLE_PLOT = 2
PROGRESS_CALLBACK_STYLE = PROGRESS_CALLBACK_STYLE_TEXT
LATEST_GITHUB_INIT_FILE = "https://raw.githubusercontent.com/MannLabs/alphatims/master/alphatims/__init__.py"


def set_logger(
    *,
    log_file_name="",
    stream: bool = True,
    log_level: int = logging.INFO,
    overwrite: bool = False,
    progress_callback: bool = True
) -> str:
    """Set the log stream and file.

    All previously set handlers will be disabled with this command.

    Parameters
    ----------
    log_file_name : str, None
        The file name to where the log is written.
        Folders are automatically created if needed.
        This is relative to the current path. When an empty string is provided,
        a log is written to the AlphaTims "logs" folder with the name
        "log_yymmddhhmmss" (reversed timestamp year to seconds).
        If None, no log file is saved.
        Default is "".
    stream : bool
        If False, no log data is sent to stream.
        If True, all logging can be tracked with stdout stream.
        Default is True.
    log_level : int
        The logging level. Usable values are defined in Python's "logging"
        module.
        Default is logging.INFO.
    overwrite : bool
        If True, overwrite the log_file if one exists.
        If False, append to this log file.
        Default is False.
    progress_callback : bool
        If True, continuous progress bars are enabled by default.
        NOTE: If stream is False, progress bars are always disabled
        Default is True.

    Returns
    -------
    : str
        The file name to where the log is written.
    """
    import time
    global PROGRESS_CALLBACK_STYLE
    root = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s> %(message)s', "%Y-%m-%d %H:%M:%S"
    )
    root.setLevel(log_level)
    while root.hasHandlers():
        root.removeHandler(root.handlers[0])
    if stream:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        root.addHandler(stream_handler)
    if log_file_name is not None:
        if log_file_name == "":
            if not os.path.exists(LOG_PATH):
                os.makedirs(LOG_PATH)
            log_file_name = LOG_PATH
        log_file_name = os.path.abspath(log_file_name)
        if os.path.isdir(log_file_name):
            current_time = time.localtime()
            current_time = "".join(
                [
                    f'{current_time.tm_year:04}',
                    f'{current_time.tm_mon:02}',
                    f'{current_time.tm_mday:02}',
                    f'{current_time.tm_hour:02}',
                    f'{current_time.tm_min:02}',
                    f'{current_time.tm_sec:02}',
                ]
            )
            log_file_name = os.path.join(
                log_file_name,
                f"log_{current_time}.txt"
            )
        directory = os.path.dirname(log_file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if overwrite:
            file_handler = logging.FileHandler(log_file_name, mode="w")
        else:
            file_handler = logging.FileHandler(log_file_name, mode="a")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    if progress_callback and stream:
        PROGRESS_CALLBACK_STYLE = PROGRESS_CALLBACK_STYLE_TEXT
    else:
        PROGRESS_CALLBACK_STYLE = PROGRESS_CALLBACK_STYLE_NONE
    return log_file_name


def show_platform_info() -> None:
    """Log all platform information.

    This is done in the following format:

        - [timestamp]> Platform information:
        - [timestamp]> system     - [...]
        - [timestamp]> release    - [...]
        - [timestamp]> version    - [...]
        - [timestamp]> machine    - [...]
        - [timestamp]> processor  - [...]
        - [timestamp]> cpu count  - [...]
        - [timestamp]> ram        - [...]/[...] Gb (available/total)
    """
    import platform
    import psutil
    logging.info("Platform information:")
    logging.info(f"system     - {platform.system()}")
    logging.info(f"release    - {platform.release()}")
    if platform.system() == "Darwin":
        logging.info(f"version    - {platform.mac_ver()[0]}")
    else:
        logging.info(f"version    - {platform.version()}")
    logging.info(f"machine    - {platform.machine()}")
    logging.info(f"processor  - {platform.processor()}")
    logging.info(
        f"cpu count  - {psutil.cpu_count()}"
        # f" ({100 - psutil.cpu_percent()}% unused)"
    )
    logging.info(
        f"ram        - "
        f"{psutil.virtual_memory().available/1024**3:.1f}/"
        f"{psutil.virtual_memory().total/1024**3:.1f} Gb "
        f"(available/total)"
    )
    logging.info("")


def show_python_info() -> None:
    """Log all Python information.

    This is done in the following format:

        - [timestamp]> Python information:
        - [timestamp]> alphatims          - [current_version]
        - [timestamp]> [required package] - [current_version]
        - ...
        - [timestamp]> [required package] - [current_version]
    """
    import importlib.metadata
    import platform
    module_versions = {
        "python": platform.python_version(),
        "alphatims": alphatims.__version__
    }
    requirements = importlib.metadata.requires("alphatims")
    for requirement in requirements:
        parts = requirement.split(";")
        if len(parts) > 1:
            if "development" in parts[1]:
                continue
            if "win32" in parts[1]:
                continue
        module_name = parts[0].split("=")[0].split()[0]
        try:
            module_version = importlib.metadata.version(module_name)
        except importlib.metadata.PackageNotFoundError:
            module_version = ""
        module_versions[module_name] = module_version
    max_len = max(len(key) for key in module_versions)
    logging.info("Python information:")
    for key, value in sorted(module_versions.items()):
        logging.info(f"{key:<{max_len}} - {value}")
    logging.info("")


def check_github_version() -> str:
    """Checks and logs the current version of AlphaTims.

    Check if the local version equals the AlphaTims GitHub master branch.
    This is only possible with an active internet connection and
    if no credentials are required for GitHub.

    Returns
    -------
    : str
        The version on the AlphaTims GitHub master branch.
        "" if no version can be found on GitHub
    """
    import urllib.request
    import urllib.error
    try:
        with urllib.request.urlopen(LATEST_GITHUB_INIT_FILE) as version_file:
            for line in version_file.read().decode('utf-8').split("\n"):
                if line.startswith("__version__"):
                    github_version = line.split()[2][1:-1]
                    if github_version != alphatims.__version__:
                        logging.info(
                            f"You are currently using AlphaTims version "
                            f"{alphatims.__version__}. "
                            f"However, the latest version of AlphaTims on "
                            f"GitHub is {github_version}. Checkout "
                            "https://github.com/MannLabs/alphatims.git "
                            "for instructions on how to update AlphaTims..."
                        )
                        logging.info("")
                    else:
                        logging.info(
                            "Current AlphaTims version is up-to-date "
                            "with GitHub."
                        )
                        logging.info("")
                    return github_version
    except IndexError:
        logging.info(
            "Could not check GitHub for the latest AlphaTims release."
        )
        logging.info("")
        return ""
    except urllib.error.URLError:
        logging.info(
            "Could not check GitHub for the latest AlphaTims release."
        )
        logging.info("")
        return ""


def save_parameters(parameter_file_name: str, paramaters: dict) -> None:
    """Save parameters to a parameter file.

    IMPORTANT NOTE: This overwrites any existing file.

    Parameters
    ----------
    parameter_file_name : str
        The file name to where the parameters are written.
    paramaters : dict
        A dictionary with parameters.
    """
    logging.info(f"Saving parameters to {parameter_file_name}")
    with open(parameter_file_name, "w") as outfile:
        json.dump(paramaters, outfile, indent=4, sort_keys=True)


def load_parameters(parameter_file_name: str) -> dict:
    """Load a parameter dict from a file.

    Parameters
    ----------
    parameter_file_name : str
        A file name that contains parameters in .json format.

    Returns
    -------
    : dict
        A dict with parameters.
    """
    with open(parameter_file_name, "r") as infile:
        return json.load(infile)


def set_threads(threads: int, set_global: bool = True) -> int:
    """Parse and set the (global) number of threads.

    Parameters
    ----------
    threads : int
        The number of threads.
        If larger than available cores, it is trimmed to the available maximum.
        If 0, it is set to the maximum cores available.
        If negative, it indicates how many cores NOT to use.
    set_global : bool
        If False, the number of threads is only parsed to a valid value.
        If True, the number of threads is saved as a global variable.
        Default is True.

    Returns
    -------
    : int
        The number of threads.
    """
    import multiprocessing
    if set_global:
        global MAX_THREADS
    max_cpu_count = multiprocessing.cpu_count()
    if threads > max_cpu_count:
        MAX_THREADS = max_cpu_count
    else:
        while threads <= 0:
            threads += max_cpu_count
        MAX_THREADS = threads
    return MAX_THREADS


def threadpool(
    _func=None,
    *,
    thread_count=None,
    progress_callback: bool = False,
) -> None:
    """A decorator that parallelizes a function with threads and callback.

    The first argument of the decorated function need to be an iterable.
    The original function should accept a single element of this iterable
    as its first argument.
    The original function cannot return values, instead it should store
    results in e.g. one if its input arrays that acts as a buffer array.

    Parameters
    ----------
    _func
        The function to decorate.
    thread_count : int, None
        The number of threads to use.
        This is always parsed with alphatims.utils.set_threads.
        Not possible as positional arguments,
        it always needs to be an explicit keyword argument.
        Default is None.
    progress_callback : bool
        If True, the default progress callback will be used as callback.
        (See "progress_callback" function.)
        If False, no callback is added.
        Default is False.

    Returns
    -------
    : function
        A parallelized decorated function.
    """
    import multiprocessing.pool
    import tqdm
    import functools

    def parallel_func_inner(func):
        def wrapper(iterable, *args, **kwargs):
            def starfunc(iterable):
                return func(iterable, *args, **kwargs)

            if thread_count is None:
                current_thread_count = MAX_THREADS
            else:
                current_thread_count = set_threads(
                    thread_count,
                    set_global=False
                )
            if progress_callback:
                progress_callback_style = PROGRESS_CALLBACK_STYLE
            else:
                progress_callback_style = PROGRESS_CALLBACK_STYLE_NONE
            with multiprocessing.pool.ThreadPool(current_thread_count) as pool:
                if progress_callback_style == PROGRESS_CALLBACK_STYLE_NONE:
                    for i in pool.imap_unordered(starfunc, iterable):
                        pass
                elif progress_callback_style == PROGRESS_CALLBACK_STYLE_TEXT:
                    with tqdm.tqdm(total=len(iterable)) as pbar:
                        for i in pool.imap_unordered(starfunc, iterable):
                            pbar.update()
                elif progress_callback_style == PROGRESS_CALLBACK_STYLE_PLOT:
                    # TODO: update?
                    with tqdm.gui(total=len(iterable)) as pbar:
                        for i in pool.imap_unordered(starfunc, iterable):
                            pbar.update()
                else:
                    raise ValueError("Not a valid progress callback style")
        return functools.wraps(func)(wrapper)
    if _func is None:
        return parallel_func_inner
    else:
        return parallel_func_inner(_func)


def njit(_func=None, *args, **kwargs):
    """A wrapper for the numba.njit decorator.

    The "cache" option is set to True by default.
    This can be overriden with kwargs.

    Parameters
    ----------
    _func
        The function to decorate.
    *args
        See numba.njit decorator.
    **kwargs
        See numba.njit decorator.

    Returns
    -------
    : function
        A numba.njit decorated function.
    """
    import numba
    if "cache" in kwargs:
        cache = kwargs.pop("cache")
    else:
        cache = True
    return numba.njit(_func, *args, cache=cache, **kwargs)


def pjit(
    _func=None,
    *,
    thread_count=None,
    cache: bool = True,
    **kwargs
):
    """A decorator that parallelizes the numba.njit decorator with threads.

    The first argument of the decorated function need to be an iterable.
    A range-object will be most performant as iterable.
    The original function should accept a single element of this iterable
    as its first argument.
    The original function cannot return values, instead it should store
    results in e.g. one if its input arrays that acts as a buffer array.
    The original function needs to be numba.njit compatible.
    Numba argument "nogil" is always set to True.

    Parameters
    ----------
    _func
        The function to decorate.
    thread_count : int, None
        The number of threads to use.
        This is always parsed with alphatims.utils.set_threads.
        Not possible as positional arguments,
        it always needs to be an explicit keyword argument.
        Default is None.
    cache : bool
        See numba.njit decorator.
        Default is True (in contrast to numba).

    Returns
    -------
    : function
        A parallelized numba.njit decorated function.
    """
    import functools
    import threading
    import numba
    import numpy as np

    def parallel_compiled_func_inner(func):
        if "cache" in kwargs:
            cache = kwargs.pop("cache")
        else:
            cache = True
        numba_func = numba.njit(nogil=True, cache=cache, **kwargs)(func)

        @numba.njit(nogil=True, cache=True)
        def numba_func_parallel(
            iterable,
            start,
            stop,
            step,
            *args,
        ):
            if len(iterable) == 0:
                for i in range(start, stop, step):
                    numba_func(i, *args)
            else:
                for i in iterable:
                    numba_func(i, *args)

        def wrapper(iterable, *args):
            if thread_count is None:
                current_thread_count = MAX_THREADS
            else:
                current_thread_count = set_threads(
                    thread_count,
                    set_global=False
                )
            threads = []
            for thread_id in range(current_thread_count):
                local_iterable = iterable[thread_id::current_thread_count]
                if isinstance(local_iterable, range):
                    start = local_iterable.start
                    stop = local_iterable.stop
                    step = local_iterable.step
                    local_iterable = np.array([], dtype=np.int64)
                else:
                    start = -1
                    stop = -1
                    step = -1
                thread = threading.Thread(
                    target=numba_func_parallel,
                    args=(
                        local_iterable,
                        start,
                        stop,
                        step,
                        *args
                    )
                )
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
                del thread
        return functools.wraps(func)(wrapper)
    if _func is None:
        return parallel_compiled_func_inner
    else:
        return parallel_compiled_func_inner(_func)


def progress_callback(iterable, style: int = -1, total: int = -1):
    """Add tqdm progress callback to iterable.

    Parameters
    ----------
    iterable
        An iterable that implements __len__.
    style : int
        The callback style. Options are:

            - -1 means to use the global PROGRESS_CALLBACK_STYLE variable.
            - PROGRESS_CALLBACK_STYLE_NONE = 0 means no callback.
            - PROGRESS_CALLBACK_STYLE_TEXT = 1 means textual callback.
            - PROGRESS_CALLBACK_STYLE_PLOT = 2 means gui callback.

        Default is -1.
    total : int
        The length of the iterable.
        If -1, this will be read as len(iterable), if __len__ is implemented.
        Default is -1.

    Returns
    -------
    : iterable
        The iterable with tqdm callback.

    Raises
    ------
    ValueError
        If no valid style (-1, 0, 1, 2) is provided.
    """
    import tqdm
    if style == -1:
        style = PROGRESS_CALLBACK_STYLE
    if style == PROGRESS_CALLBACK_STYLE_NONE:
        return iterable
    elif style == PROGRESS_CALLBACK_STYLE_TEXT:
        if total != -1:
            return tqdm.tqdm(iterable, total=total)
        else:
            return tqdm.tqdm(iterable)
    elif style == PROGRESS_CALLBACK_STYLE_PLOT:
        # TODO: update?
        return tqdm.gui.tqdm(iterable)
    else:
        raise ValueError("Not a valid progress callback style")


def create_hdf_group_from_dict(
    hdf_group,
    data_dict: dict,
    *,
    overwrite: bool = False,
    compress: bool = False,
    recursed: bool = False,
    chunked: bool = False
) -> None:
    """Save a dict to an open hdf group.

    Parameters
    ----------
    hdf_group : h5py.File.group
        An open and writable HDF group.
    data_dict : dict
        A dict that needs to be written to HDF.
        Keys always need to be strings. Values are stored as follows:

            - subdicts -> subgroups.
            - np.array -> array
            - pd.dataframes -> subdicts with "is_pd_dataframe: True" attribute.
            - bool, int, float and str -> attrs.
            - None values are skipped and not stored explicitly.

    overwrite : bool
        If True, existing subgroups, arrays and attrs are fully
        truncated/overwritten.
        If False, the existing value in HDF remains unchanged.
        Default is False.
    compress : bool
        If True, all arrays are compressed with binary shuffle and "lzf"
        compression.
        If False, arrays are saved as provided.
        On average, compression halves file sizes,
        at the cost of 2-10 time longer accession times.
        Default is False.
    recursed : bool
        If False, the default progress callback is added while itereating over
        the keys of the data_dict.
        If True, no callback is added, allowing subdicts to not trigger
        callback.
        Default is False.
    chunked : bool
        If True, all arrays are chunked.
        If False, arrays are saved as provided.
        Default is False.

    Raises
    ------
    ValueError
        When a value of data_dict cannot be converted to an HDF value
        (see data_dict).
    KeyError
        When a key of data_dict is not a string.
    """
    import pandas as pd
    import numpy as np
    import h5py
    if recursed:
        iterable_dict = data_dict.items()
    else:
        iterable_dict = progress_callback(data_dict.items())
    for key, value in iterable_dict:
        if not isinstance(key, str):
            raise KeyError(f"Key {key} is not a string.")
        if isinstance(value, pd.core.frame.DataFrame):
            new_dict = {key: dict(value)}
            new_dict[key]["is_pd_dataframe"] = True
            create_hdf_group_from_dict(
                hdf_group,
                new_dict,
                overwrite=overwrite,
                recursed=True,
                compress=compress,
                chunked=chunked,
            )
        elif isinstance(value, (np.ndarray, pd.core.series.Series)):
            if isinstance(value, (pd.core.series.Series)):
                value = value.values
            if overwrite and (key in hdf_group):
                del hdf_group[key]
            if key not in hdf_group:
                if value.dtype.type == np.str_:
                    value = value.astype(np.dtype('O'))
                if value.dtype == np.dtype('O'):
                    hdf_group.create_dataset(
                        key,
                        data=value,
                        dtype=h5py.string_dtype()
                    )
                else:
                    hdf_group.create_dataset(
                        key,
                        data=value,
                        compression="lzf" if compress else None,
                        # compression="gzip" if compress else None, # TODO slower to make, faster to load?
                        shuffle=compress,
                        chunks=True if chunked else None,
                    )
        elif isinstance(value, (bool, int, float, str)):
            if overwrite or (key not in hdf_group.attrs):
                hdf_group.attrs[key] = value
        elif isinstance(value, dict):
            if key not in hdf_group:
                hdf_group.create_group(key)
            create_hdf_group_from_dict(
                hdf_group[key],
                value,
                overwrite=overwrite,
                recursed=True,
                compress=compress,
            )
        elif value is None:
            continue
        else:
            raise ValueError(
                f"The type of {key} is {type(value)}, which "
                "cannot be converted to an HDF value."
            )


def create_dict_from_hdf_group(hdf_group) -> dict:
    """Convert the contents of an HDF group and return as normal Python dict.

    Parameters
    ----------
    hdf_group : h5py.File.group
        An open and readable HDF group.

    Returns
    -------
    : dict
        A Python dict.
        Keys of the dict are names of arrays, attrs and subgroups.
        Values are corresponding arrays and attrs.
        Subgroups are converted to subdicts.
        If a subgroup has an "is_pd_dataframe=True" attr,
        it is automatically converted to a pd.dataFrame.

    Raises
    ------
    ValueError
        When an attr value in the HDF group is not an int, float, str or bool.
    """
    import h5py
    import pandas as pd
    import numpy as np
    result = {}
    for key in hdf_group.attrs:
        value = hdf_group.attrs[key]
        if isinstance(value, np.integer):
            result[key] = int(value)
        elif isinstance(value, np.float64):
            result[key] = float(value)
        elif isinstance(value, (str, bool, np.bool_)):
            result[key] = value
        else:
            raise ValueError(
                f"The type of {key} is {type(value)}, which "
                "cannot be converted properly."
            )
    for key in hdf_group:
        subgroup = hdf_group[key]
        if isinstance(subgroup, h5py.Dataset):
            result[key] = subgroup[:]
        else:
            if "is_pd_dataframe" in subgroup.attrs:
                result[key] = pd.DataFrame(
                    {
                        column: subgroup[column][:] for column in sorted(
                            subgroup
                        )
                    }
                )
            else:
                result[key] = create_dict_from_hdf_group(hdf_group[key])
    return result


class Option_Stack(object):
    """A stack with the option to redo and undo."""

    def __init__(self, option_name: str, option_initial_value):
        """Create an option stack.

        Parameters
        ----------
        option_name : str
            The name of this option.
        option_initial_value : type
            The initial value of this stack.
            Can be any object that supports the "!=" operator.
        """
        self._stack = [option_initial_value]
        self._stack_pointer = 0
        self._option_name = option_name

    @property
    def current_value(self):
        """: type : The current value of this stack."""
        return self._stack[self._stack_pointer]

    @property
    def size(self) -> int:
        """: int : The size of this stack without the initial value."""
        return len(self._stack) - 1

    @property
    def option_name(self) -> str:
        """: str : The name of this stack."""
        return self._option_name

    def update(self, option_value) -> bool:
        """Update this stack with the value.

        Parameters
        ----------
        option_value : type
            An value to add to this stack.
            Can be any object that supports the "!=" operator.

        Returns
        -------
        bool
            True if the stack was updated.
            False if the provided value equald the current value of this stack.
        """
        if self.current_value != option_value:
            self.trim()
            self._stack.append(option_value)
            self._stack_pointer += 1
            return True
        return False

    def redo(self):
        """Increase the stack pointer with 1.

        Returns
        -------
        type
            None if the pointer was already at the maximum.
            Otherwise the new value if the pointer was increased.
        """
        if self._stack_pointer < self.size:
            self._stack_pointer += 1
            return self.current_value
        return None

    def undo(self):
        """Reduce the stack pointer with 1.

        Returns
        -------
        type
            None if the pointer was already at the maximum.
            Otherwise the new value if the pointer was reduced.
        """
        if self._stack_pointer > 0:
            self._stack_pointer -= 1
            return self.current_value
        return None

    def trim(self) -> bool:
        """Remove all elements above of the current stack pointer

        Returns
        -------
        bool
            True if something was removed,
            i.e. if stack pointer was not at the top.
            False if nothing could be deleted,
            i.e. the stack pointer was at the top.
        """
        if self._stack_pointer != self.size:
            self._stack = self._stack[:self._stack_pointer + 1]
            return True
        return False

    def __str__(self):
        return f"{self._stack_pointer} {self._option_name} {self._stack}"


class Global_Stack(object):
    """A stack that holds multiple option stacks.

    The current value of each option stack can be retrieved by indexing,
    i.e. option_value = self[option_key].
    """

    def __init__(self, all_available_options: dict):
        """Create a global stack.

        Parameters
        ----------
        all_available_options : dict
            A dictionary whose items are (str, type),
            which can be used to create an Option_Stack.
        """
        self._option_stacks = {
            option_key: Option_Stack(
                option_key,
                option_value
            ) for option_key, option_value in all_available_options.items()
        }
        self._number_of_options = len(all_available_options)
        self._stack_pointer = 0
        self._stack = [None]
        self._is_locked = False
        self._key = -1

    @property
    def is_locked(self):
        """: bool : A flag to check if this stack is modifiable"""
        return self._is_locked

    @contextlib.contextmanager
    def lock(self):
        """A context manager to lock this stack and prevent modification."""
        import random
        key = random.random()
        try:
            if self._key == -1:
                self._key = key
            self._is_locked = True
            yield self
        finally:
            if self._key == key:
                self._is_locked = False
                self._key = -1

    @property
    def current_values(self) -> dict:
        """: dict : A dict with (option_key: option_value) mapping."""
        return {
            option_key: option_stack.current_value for (
                option_key,
                option_stack
            ) in self._option_stacks.items()
        }

    @property
    def size(self):
        """: int : The size of this stack without the initial value."""
        return len(self._stack) - 1

    def __getitem__(self, key: str):
        return self._option_stacks[key].current_value

    def update(self, option_key: str, option_value) -> tuple:
        """Update an option stack with a value.

        Parameters
        ----------
        option_key : str
            The name of the option stack to update.
        option_value : type
            An value to add to this stack.
            Can be any object that supports the "!=" operator.

        Returns
        -------
        tuple
            ("", None) if the pointer was not updated,
            i.e. the latest update was equal to the current update.
            Otherwise (option_name, new_value).
        """
        if self.is_locked:
            return "", None
        current_value = self[option_key]
        if current_value == option_value:
            return "", None
        self._option_stacks[option_key].update(option_value)
        self.trim()
        self._stack_pointer += 1
        self._stack.append(option_key)
        return option_key, option_value

    def redo(self) -> tuple:
        """Increase the stack pointer with 1.

        Returns
        -------
        tuple
            ("", None) if the pointer was already at the maximum.
            Otherwise (option_name, new_value) if the pointer was increased.
        """
        if self.is_locked:
            return "", None
        if self._stack_pointer < self.size:
            self._stack_pointer += 1
            option_key = self._stack[self._stack_pointer]
            option_value = self._option_stacks[option_key].redo()
            if option_value is not None:
                return option_key, option_value
        return "", None

    def undo(self) -> tuple:
        """Reduce the stack pointer with 1.

        Returns
        -------
        tuple
            ("", None) if the pointer was already at the maximum.
            Otherwise (option_name, new_value) if the pointer was reduced.
        """
        if self.is_locked:
            return "", None
        if self._stack_pointer > 0:
            option_key = self._stack[self._stack_pointer]
            self._stack_pointer -= 1
            option_value = self._option_stacks[option_key].undo()
            if option_value is not None:
                return option_key, option_value
        return "", None

    def trim(self) -> bool:
        """Remove all elements above of the current stack pointer

        Returns
        -------
        bool
            True if something was removed,
            i.e. if stack pointer was not at the top.
            False if nothing could be deleted,
            i.e. the stack pointer was at the top.
        """
        if self._stack_pointer != self.size:
            self._stack = self._stack[:self._stack_pointer + 1]
            for stack in self._option_stacks.values():
                stack.trim()
            return True
        return False

    def __str__(self):
        result = " ".join(
            [
                str(stack) for stack in self._option_stacks.values()
            ]
        )
        # values = str(self.current_values)
        return result + " " + " ".join(
            [
                str(self._stack_pointer),
                "global",
                str(self._stack)
            ]
        )


set_threads(MAX_THREADS)
# set_logger(log_file_name=None)
