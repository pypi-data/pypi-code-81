""" file format input output realization with meta info """

from os.path import dirname, basename, isfile, join
from pathlib import Path
import importlib
from inspect import isclass, getmembers
import glob

from apu.io.format.csv import CSV
from apu.io.format.dill import DILL
from apu.io.format.h5 import H5
from apu.io.format.json import (JSON, JSONL)
from apu.io.format.matlab import MAT
from apu.io.format.np import (NPY, NPZ)
from apu.io.format.pickel import PICKLE
from apu.io.format.yaml import YAML

__all__ = [
    "CSV", "DILL", "H5", "JSON", "JSONL", "MAT", "NPZ", "NPY", "PICKLE", "YAML"
]

__supported_format__ = {}

def supported_format():
    """ give supported formats """
    if not bool(__supported_format__):
        modules = glob.glob(join(dirname(__file__), "*.py"))
        module_name = [Path(local_file) for local_file \
                     in modules if not '__init__' in local_file]

        # import module
        for module in module_name:
            mod_gen = importlib.import_module(
                f"apu.io.__fileformat.{module.stem}")

            for _, obj in getmembers(mod_gen, isclass):
                if "apu.io.__fileformat" not in obj.__module__:
                    continue

                __supported_format__[f"{obj.suffix()}"] = obj

    return __supported_format__
