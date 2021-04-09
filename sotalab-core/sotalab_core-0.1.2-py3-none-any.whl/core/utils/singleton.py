from typing import Any, Dict


class Singleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__()
        return cls._instances[cls]
