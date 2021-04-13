__all__ = ['expand_path']

import os
import re
import subprocess
import tempfile
import pandas as pd

EPLUS_EXEC = "energyplus"


IDF_GENERATED_FILE_NAME = "generated_input.idf"

def expand_path(path):
    """Expand `~` constructs and return an absolute path.

    On Unix operating systems (Linux, MacOSX, ...),
    `~` is a shortcut for the curent user's home directory
    (e.g. "/home/jack" for "jack").

    Example
    -------

    Lets assume we are on a Unix system,
    the current user is "jack" and the current path is "/bar".

    >>> expand_path("~/foo")
    "/home/jack/foo"

    >>> expand_path("baz")
    "/bar/baz"

    >>> expand_path("../tmp")
    "/tmp"

    Parameters
    ----------
    path : str
        The `path` to expand.

    Returns
    -------
    str
        The absolute and expanded `path`.
    """
    if path is not None:
        path = os.path.expanduser(path)  # to handle "~/..." paths
        path = os.path.abspath(path)     # to handle relative paths
        return path
    else:
        return None


def sub_run(orig_idf_path, weather_file_path, sub_dict={}, verbose=False):
    """Substitute IDF input and run eplus"""

    # CHECK sub_dict ##########################################################

    all_seq = all([type(v) in (list, tuple) and len(v) > 1 for v in sub_dict.values()])

    if all_seq:
        val_len = [len(v) for v in sub_dict.values()]
        assert min(val_len) == max(val_len)

    # RUN

    if all_seq:
        list_of_dict = [dict(zip(sub_dict, t)) for t in zip(*sub_dict.values())]
        res = [sub_one_field_and_run(orig_idf_path, weather_file_path, sub_dict2, verbose=verbose) for sub_dict2 in list_of_dict]
    else:
        res = sub_one_field_and_run(orig_idf_path, weather_file_path, sub_dict, verbose=verbose)
    
    return res


def sub_one_field(orig_idf_path, sub_dict={}, verbose=False):
    """Substitute IDF input and run eplus"""

    for k, v in sub_dict.items():
        if type(v) in (list, tuple) and len(v) == 1:
            sub_dict[k] = v[0]
    
    # CHECK sub_dict ##########################################################

    all_scalar = all([type(v) in (int, float, bool, str) for v in sub_dict.values()])
    assert all_scalar

    # READ THE ORIGINAL INPUT FILE ############################################

    idf_str = None
    orig_idf_path = expand_path(orig_idf_path)

    with open(orig_idf_path) as fd:
        idf_str = fd.read()

    # MODIFY THE INPUT FILE ###################################################

    for (obj, name, field), value in sub_dict.items():
        idf_str = re_substitute(idf_str, obj, name, field, value)

    return idf_str


def sub_one_field_and_run(orig_idf_path, weather_file_path, sub_dict={}, verbose=False):
    """Substitute IDF input and run eplus"""

    idf_str = sub_one_field(orig_idf_path, sub_dict=sub_dict, verbose=verbose)

    # WRITE THE MODIFIED INPUT FILE ###########################################

    home_path = expand_path("~")

    with tempfile.TemporaryDirectory(dir=home_path, prefix=".", suffix="_test") as temp_dir_path:
        dst_idf_path = os.path.join(temp_dir_path, IDF_GENERATED_FILE_NAME)

        if verbose:
            print("Write", dst_idf_path)

        with open(dst_idf_path, "w") as fd:
            fd.write(idf_str)

        if verbose:
            print(idf_str)

        df = run_eplus(dst_idf_path, weather_file_path=weather_file_path)

    return df


def re_substitute(s, obj, name, field, value):
    # C.f. https://www.thegeekstuff.com/2014/07/advanced-python-regex/
    #return re.sub(r'(?P<g1>' + obj + r'.*?)(?P<g2>' + name + r'.*?)(\d+.?\d*|\w+)(?P<g3>(,|;) +!- ' + field + ')',
    #              r'\g<g1>\g<g2>' + str(value) + r'\g<g3>',
    #              s,
    #              flags=re.MULTILINE|re.DOTALL)
    return re.sub(r'(?P<g1>' + obj + r'.*?)(?P<g2>' + name + r'.*?^ *)[^,;]+(?P<g3>(,|;) +!- ' + field + ')',
                  r'\g<g1>\g<g2>' + str(value) + r'\g<g3>',
                  s,
                  flags=re.MULTILINE|re.DOTALL)


def run_eplus(idf_file_path, weather_file_path, output_directory_path="."):
    """
    energyplus --help
    EnergyPlus, Version 9.4.0-998c4b761e
    PythonLinkage: Linked to Python Version: "3.6.9 (default, Jul 17 2020, 12:50:27) 
    [GCC 8.4.0]"
    Usage: energyplus [options] [input-file]
    Options:
    -a, --annual                 Force annual simulation
    -c, --convert                Output IDF->epJSON or epJSON->IDF, dependent on
                                input file type
    -D, --design-day             Force design-day-only simulation
    -d, --output-directory ARG   Output directory path (default: current
                                directory)
    -h, --help                   Display help information
    -i, --idd ARG                Input data dictionary path (default: Energy+.idd
                                in executable directory)
    -m, --epmacro                Run EPMacro prior to simulation
    -p, --output-prefix ARG      Prefix for output file names (default: eplus)
    -r, --readvars               Run ReadVarsESO after simulation
    -s, --output-suffix ARG      Suffix style for output file names (default: L)
                                    L: Legacy (e.g., eplustbl.csv)
                                    C: Capital (e.g., eplusTable.csv)
                                    D: Dash (e.g., eplus-table.csv)
    -v, --version                Display version information
    -w, --weather ARG            Weather file path (default: in.epw in current
                                directory)
    -x, --expandobjects          Run ExpandObjects prior to simulation
    --convert-only                 Only convert IDF->epJSON or epJSON->IDF,
                                dependent on input file type. No simulation
    Example: energyplus -w weather.epw -r input.idf

    """

    idf_file_path = expand_path(idf_file_path)
    weather_file_path = expand_path(weather_file_path)
    output_directory_path = expand_path(output_directory_path)

    cmd = [
            EPLUS_EXEC,
            "-w", weather_file_path,
            "-d", output_directory_path,
            "-r",
            idf_file_path
          ]

    print(" ".join(cmd))

    subprocess.call(cmd)

    df = pd.read_csv(os.path.join(output_directory_path, "eplusout.csv"))

    return df