import collections
import datetime
import errno
import os
import tempfile

import cv2


####
#%%% OpenCV-related
####


def cv2_version():
    return tuple(int(value) for value in cv2.__version__.split("."))


####
#%%% file-related
####


def mkdir(dirname):
    """
    Create the given directory if it does not already exist.
    """
    
    if dirname == "":
        return
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_temp_dir(prefix):
    """
    Creates and returns temporary directory.

    The property `.name` holds the path. It can be deleted using the `.cleanup()` method.
    """
    return tempfile.TemporaryDirectory(prefix=prefix)


def human_bytes(byte_count):
    """
    Formats a given `byte_count` into a human-readable string.
    """

    prefixes = collections.OrderedDict()
    prefixes["KiB"] = 1024.0**1
    prefixes["MiB"] = 1024.0**2
    prefixes["GiB"] = 1024.0**3

    count = byte_count
    unit = "bytes"
    for (new_unit, new_scale) in prefixes.items():
        new_count = byte_count / new_scale
        if new_count < 1.0:
            break
        else:
            count = new_count
            unit = new_unit

    if isinstance(count, int):
        # count is an integer -> use no decimal places
        return "{} {}".format(count, unit)
    else:
        # count is a float -> use two decimal places
        return "{:.2f} {}".format(count, unit)


####
#%%% output-related
####


def now_str(mode="compact", date=True, time=True, microtime=True):
    """
    Return the current date and/or time as string.
    """

    # check arguments
    if not (date or time or microtime):
        raise ValueError("At least one of 'date', 'time', 'microtime' must be `True`")

    # select format string parts based on mode
    if mode == "compact":
        date_fmt = "%Y%m%d"
        time_sep = "_"
        time_fmt = "%H%M%S"
        micro_sep = "_"
        micro_fmt = "%f"
    elif mode == "readable":
        date_fmt = "%Y-%m-%d"
        time_sep = "_"
        time_fmt = "%H-%M-%S"
        micro_sep = "_"
        micro_fmt = "%f"
    elif mode == "print":
        date_fmt = "%Y-%m-%d"
        time_sep = " "
        time_fmt = "%H:%M:%S"
        micro_sep = "."
        micro_fmt = "%f"
    else:
        raise ValueError("Invalid mode '{}".format(mode))

    # build final format string
    fmt = ""
    if date:
        fmt += date_fmt
    if time:
        if fmt != "":
            fmt += time_sep
        fmt += time_fmt
    if microtime:
        if fmt != "":
            fmt += micro_sep
        fmt += micro_fmt

    # return formatted date and/or time
    return datetime.datetime.now().strftime(fmt)


def ftable(rows):
    """
    Format the data specified in `rows` as table string.
    """
    
    col_sep = "  "
    sep_symbol = "-"
    
    # count the max length for each column
    col_count = max(len(row) for row in rows)
    col_lengths = [0] * col_count
    for row in rows:
        for n_col in range(col_count):
            col_lengths[n_col] = max(col_lengths[n_col], len(str(row[n_col])))

    # the line at the top and bottom
    sep_line = col_sep.join(sep_symbol * col_length for col_length in col_lengths)
    
    # transform rows into lines
    lines = []
    lines.append(sep_line)
    for row in rows:
        col_strs = []
        for (col_length, col) in zip(col_lengths, row):
            col_str = "{{: <{}}}".format(col_length).format(str(col))
            col_strs.append(col_str)
        lines.append(col_sep.join(col_strs))
    lines.append(sep_line)
    
    # return table as single string
    return "\n".join(lines)
    

def ptable(rows, **kwargs):
    """
    Print the data specified in `rows` as table.
    """
    
    print(ftable(rows=rows), **kwargs)
