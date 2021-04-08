import inspect
import sys

from grebble_flow.processors.base import BaseFlowProcessor


def import_processors():
    module = "processors"
    module_path = module

    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=[module])


def find_all_processors():
    import_processors()
    inspect.getmembers(import_processors())
    result = [cls for cls in BaseFlowProcessor.__subclasses__()]
    return result
