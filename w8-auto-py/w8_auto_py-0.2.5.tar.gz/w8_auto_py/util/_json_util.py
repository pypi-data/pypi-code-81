# @Time     : 2021/3/27
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import typing

try:
    import simplejson as json
except ImportError:
    import json

from w8_auto_py.typings import PyObject, PathType
from w8_auto_py.global_vars import G_ENCODING


class JsonUtil:

    @classmethod
    def to_json(cls,
                obj: PyObject,
                encoding: str = G_ENCODING,
                ensure_ascii: bool = False,
                **kwargs) -> str:
        """
        python object -> JSON
        :return:
        :param obj:
        :param encoding:
        :param ensure_ascii:
        :param kwargs:
        :return: str
        """
        try:
            return json.dumps(obj,
                              encoding=encoding,
                              ensure_ascii=ensure_ascii,
                              **kwargs)
        except Exception as e:
            raise ValueError(f"json 解析失败 {e}")

    @classmethod
    def to_dict(cls,
                json_string: str,
                encoding: str = G_ENCODING,
                **kwargs) -> typing.Dict[str, typing.Any]:
        """
        JSON -> python dict
        :param json_string:
        :param encoding:
        :param kwargs:
        :return: dict
        """
        if not json_string:
            return {}

        if isinstance(json_string, dict):
            return json_string

        try:
            return json.loads(json,
                              encoding=encoding,
                              **kwargs)

        except json.JSONDecodeError as e:
            raise ValueError(f"JSON to python dict error: {e}")

    @classmethod
    def to_file(cls,
                obj: PyObject,
                file: PathType,
                encoding: str = G_ENCODING,
                ensure_ascii: bool = False,
                indent: int = 4) -> None:
        """
        写入文件
        Args:
            obj:
            file:
            encoding:
            ensure_ascii:
            indent:

        Returns:

        """
        with open(file, mode="w", encoding=encoding) as f:
            json.dump(obj, f, ensure_ascii=ensure_ascii, indent=indent)
