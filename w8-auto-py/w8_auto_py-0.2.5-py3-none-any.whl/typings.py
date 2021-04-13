# @Time     : 2021/3/26
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import sys
import typing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path

"""
全局类型文件
"""

_AnyStringMapping = typing.Mapping[str, typing.AnyStr]
_AnyStringDict = typing.Dict[str, typing.AnyStr]

PyObject = typing.Union[
    _AnyStringMapping, _AnyStringDict,
    typing.List[_AnyStringMapping], typing.List[_AnyStringDict],
    typing.Tuple[_AnyStringMapping], typing.Tuple[_AnyStringDict]
]

Function = typing.Callable
FunctionMap = typing.Dict[typing.Any, Function]
FunctionIterable = typing.Iterable[Function]
FunctionList = typing.List[Function]
FunctionSet = typing.Set[Function]

ArgsType = typing.Tuple[typing.Any]
KwargsType = typing.Dict[str, typing.Any]
NumberTypes = typing.Union[int, float]

PoolExecutorTypes = typing.Union[
    ThreadPoolExecutor,
    ProcessPoolExecutor
]

PathType = typing.Union[str, Path]

_PY_3743 = (3, 7, 4, 3)
_PY_38 = (3, 8)
Interface = object

if sys.version_info >= _PY_38:
    Interface = typing.Protocol

else:
    try:
        import typing_extensions

        Interface = typing_extensions.Protocol
    except ImportError:
        pass
