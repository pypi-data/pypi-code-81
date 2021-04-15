"""
savely write and read pickle files
"""

import inspect
import cloudpickle
import pickle
import gzip
import lzma
import bz2
import os
import json
from uuid import UUID
import rapidjson

from loris import ignore
from loris.errors import LorisSerializationError


_DEFAULT_EXTENSION_MAP = {
    "gz": "gzip",
    "gzip": "gzip",
    "bz": "bz2",
    "bz2": "bz2",
    "lzma": "lzma",
    "pkl": "pickle"
}


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def string_dump(obj):
    return rapidjson.dumps(
        obj,
        uuid_mode=rapidjson.UM_CANONICAL,
        datetime_mode=rapidjson.DM_ISO8601
    )


def string_load(string):
    return rapidjson.loads(
        string.replace("'", '"'),
        uuid_mode=rapidjson.UM_CANONICAL,
        datetime_mode=rapidjson.DM_ISO8601
    )


def infer_compression_from_filename(filename: str) -> str:
    """Return the compression protocal inferred from given filename.
    Parameters
    ----------
    filename: str
        The filename for which to infer the compression protocol
    """
    return _DEFAULT_EXTENSION_MAP.get(filename.split(".")[-1], None)


def spickledumps(obj):
    """saver pickle.dumps for relative imports
    """
    # TODO doesn't work across unix and windows together
    # TODO doesn't work properly if sys path was modified!
    module = inspect.getmodule(obj)
    # if isnstance
    if module is None:
        module = inspect.getmodule(type(obj))

    # package name
    package_name = module.__name__.split('.')[0]
    # __main__ handled separately
    if package_name == '__main__':
        return b"\0" + cloudpickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    # cwd and modulepath
    cwd = os.getcwd()
    modulepath = module.__file__
    relativepath = os.path.split(modulepath)[-1]
    # assume import of python folder from working directory
    if modulepath.startswith(cwd) and os.path.exists(package_name):
        folder_data = {}
        for root, d_names, f_names in os.walk(package_name):
            folder_name = os.path.split(root)[-1]
            if (
                folder_name in ignore.ignore_folder
                or folder_name.endswith(ignore.ignore_folder_endings)
                or folder_name.endswith(ignore.ignore_folder_starts)
            ):
                # skip unnecessary folders
                continue
            # save only allowed files
            f_names = [
                name for name in f_names
                if not (
                    name in ignore.ignore_file
                    or name.endswith(ignore.ignore_file_endings)
                    or name.startswith(ignore.ignore_file_starts)
                )
            ]
            for f_name in f_names:
                f_path = os.path.join(root, f_name)

                with open(f_path, "r") as f:
                    contents = f.read()

                folder_data[f_path] = contents
        folder_bytes = pickle.dumps(
            folder_data, protocol=pickle.HIGHEST_PROTOCOL
        )
        data_bytes = cloudpickle.dumps(
            obj, protocol=pickle.HIGHEST_PROTOCOL
        )
        return b"\1" + pickle.dumps(
            (folder_bytes, data_bytes),
            protocol=pickle.HIGHEST_PROTOCOL
        )

    # assume import of python file from working directory
    elif modulepath.startswith(cwd) and os.path.exists(relativepath):
        with open(relativepath, "r") as f:
            contents = f.read()

        folder_bytes = pickle.dumps(
            {relativepath: contents}, protocol=pickle.HIGHEST_PROTOCOL
        )
        data_bytes = cloudpickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        return b"\1" + pickle.dumps(
            (folder_bytes, data_bytes),
            protocol=pickle.HIGHEST_PROTOCOL
        )
    else:
        # just use pickledumps
        return b"\0" + cloudpickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)


def spickleloads(binary):
    """saver pickle.loads for relative imports
    """

    number = binary[0]
    data = pickle.loads(binary[1:])

    if not number:
        return data

    elif number == 1:
        folder_data = pickle.loads(data[0])
        for f_path, contents in folder_data.items():
            f_path = os.path.normpath(f_path)
            # create files in cwd if they do not exist
            if os.path.exists(f_path):
                continue

            root, f_name = os.path.split(f_path)

            # create root directories
            if not os.path.exists(root):
                os.makedirs(root)

            # write files
            with open(f_path, "w") as f:
                f.write(contents)

        return pickle.loads(data[1])

    else:
        raise LorisSerializationError(
            f"Unknown byte identifier number: '{number}'."
        )


def get_file_object(filename, mode="rb"):

    compression = infer_compression_from_filename(filename)
    if compression is None or compression == "pickle":
        file = open(filename, mode=mode)
    elif compression == "gzip":
        file = gzip.open(filename, mode=mode)
    elif compression == "bz2":
        file = bz2.open(filename, mode=mode)
    elif compression == "lzma":
        file = lzma.open(filename, mode=mode)
    else:
        raise LorisSerializationError(
            f"Compression type '{compression}' does not exist."
        )

    return file


def write_pickle(filename, data):
    """
    write pickled file
    """

    with get_file_object(filename, mode="wb") as f:
        f.write(spickledumps(data))


def read_pickle(filename):
    """
    read pickled file
    """

    with get_file_object(filename, mode="rb") as f:
        data = spickleloads(f.read())

    return data
