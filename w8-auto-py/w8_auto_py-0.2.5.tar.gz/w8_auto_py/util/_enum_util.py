# @Time     : 2021/3/27
# @Project  : w8_auto_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import enum
import typing

EnumValue = typing.TypeVar("EnumValue")


class EnumUtil(object):

    @staticmethod
    def create_dict_by_enum(enums: enum.Enum) -> typing.Dict:
        """
        通过枚举创建字典
        :param enums:
        :return:
        """
        if not issubclass(enums, enum.Enum):
            raise TypeError(f"{enums} 需要一个枚举类")

        return {item: item.value for _, item in enumerate(enums)}

    @staticmethod
    def get_enum_key(mapping: dict, key: enum.Enum) -> EnumValue:
        """
        获取枚举 key
        :param mapping:
        :param key:
        :return:
        """
        if not isinstance(key, enum.Enum):
            raise TypeError(f"{key} 需要一个枚举对象")

        if not isinstance(mapping, dict):
            mapping = {}

        return mapping.get(key)

    @staticmethod
    def get_enum_value(enums: enum.Enum) -> EnumValue:
        """
        获取枚举值
        :param enums:
        :return:
        """
        if not isinstance(enums, enum.Enum):
            raise TypeError(f"{enums} 需要一个枚举对象")

        return enums.value
