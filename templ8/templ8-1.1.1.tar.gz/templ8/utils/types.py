from inspect import signature
from typing import Any, Dict, List


def init_keys(cls: Any) -> List[str]:
    return list(signature(cls.__init__).parameters.keys())


def filter_dataclass_input(
    cls: Any, dct: Dict[str, Any]
) -> Dict[str, Any]:
    return dict(
        filter(
            lambda x: x[0] in init_keys(cls),
            dct.items(),
        )
    )
