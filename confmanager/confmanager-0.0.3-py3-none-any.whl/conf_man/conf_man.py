# -*- coding:utf-8 -*-
# @Author   : Haogooder
# @Date     : 2021/4/5 4月 05 2021
# @Software : PyCharm
# @FileName : conf_man
# @Desc     : The description of this file
import argparse
import json
import os
from typing import Dict, List, Set, Optional

import yaml


class ConfError(RuntimeError):
    pass


class ConfMan:
    """
    Config Manager
    """
    _EXPLICIT_SETS_: Dict[str, str]
    _ENV_BIND_MAPS_: Dict[str, str]
    _FLAG_BIND_MAPS_: Dict[str, str]
    _ENV_PREFIX_: Optional[str]
    _CONF_FILE_DIRS_: List[str]
    _CONF_FILE_NAME_: Optional[str]
    _CONF_FILE_TYPE_: Optional[str]
    _CONF_TYPE_SUPPORTS_: List[str]
    _DEFAULTS_: Dict[str, str]

    _EXPLICIT_SETS_ = {}
    _ENV_BIND_MAPS_ = {}
    _FLAG_BIND_MAPS_ = {}
    _CONF_FILE_DIRS_ = []
    _DEFAULTS_ = {}

    _ENV_PREFIX_: Optional[str] = None
    _CONF_TYPE_SUPPORTS_ = ["json", "yaml"]
    _CONF_FILE_NAME_ = None
    _CONF_FILE_TYPE_ = None

    @classmethod
    def clear(cls):
        cls._EXPLICIT_SETS_ = {}
        cls._ENV_BIND_MAPS_ = {}
        cls._FLAG_BIND_MAPS_ = {}
        cls._CONF_FILE_DIRS_ = []
        cls._DEFAULTS_ = {}
        cls._ENV_PREFIX_ = None
        cls._CONF_FILE_NAME_ = None
        cls._CONF_FILE_TYPE_ = None

    @classmethod
    def set(cls, key: str, val: str):
        if not isinstance(val, str):
            raise ConfError("显式设置仅仅支持字符串类型的值")
        cls._EXPLICIT_SETS_.update({key: val})

    @classmethod
    def set_env_prefix(cls, prefix: str):
        cls._ENV_PREFIX_ = prefix.upper()

    @classmethod
    def bind_env(cls, key: str, name: str):
        cls._ENV_BIND_MAPS_.update({key: name.upper()})

    @classmethod
    def bind_flag(cls, key: str, name: str):
        cls._FLAG_BIND_MAPS_.update({key: name})

    @classmethod
    def add_conf_dir(cls, path: str):
        cls._CONF_FILE_DIRS_.append(path)

    @classmethod
    def set_conf_file_name(cls, filename: str):
        cls._CONF_FILE_NAME_ = filename

    @classmethod
    def set_conf_file_type(cls, filetype: str):
        if filetype not in cls._CONF_TYPE_SUPPORTS_:
            raise ConfError("配置文件类型不支持，目前支持: json / yaml")
        cls._CONF_FILE_TYPE_ = filetype

    @classmethod
    def set_default(cls, key: str, default: str):
        if not isinstance(default, str):
            raise ConfError("默认值仅仅支持字符串类型的值")
        cls._DEFAULTS_.update({key: default})

    @classmethod
    def _get_by_env_(cls, key: str) -> Optional[str]:
        env_name: Optional[str]
        env_key: Optional[str]
        env_name = cls._ENV_BIND_MAPS_.get(key)
        if env_name and cls._ENV_PREFIX_:
            env_key = "{0}_{1}".format(cls._ENV_PREFIX_, env_name).upper()
        elif env_name and not cls._ENV_PREFIX_:
            env_key = env_name.upper()
        else:
            env_key = None
        if env_key is None:
            return None
        val = os.getenv(env_key)
        return val

    @classmethod
    def _get_by_cli_(cls, key: str) -> Optional[str]:
        flag_name: Optional[str]
        flag_name = cls._FLAG_BIND_MAPS_.get(key)
        if flag_name is None:
            return None
        flag_name_with_prefix = "--{0}".format(flag_name)
        parser = argparse.ArgumentParser()
        parser.add_argument(flag_name_with_prefix, required=False)
        args, _ = parser.parse_known_args()
        val = args.__dict__.get(flag_name)
        return val

    @classmethod
    def _get_by_file_(cls, key: str) -> Optional[str]:
        file_path: str
        file_content: dict
        file_content = {}
        if len(cls._CONF_FILE_DIRS_) == 0 or cls._CONF_FILE_NAME_ is None or cls._CONF_FILE_TYPE_ is None:
            return None
        for file_dir in cls._CONF_FILE_DIRS_:
            file_path = os.path.join(file_dir, cls._CONF_FILE_NAME_)
            try:
                with open(file_path, mode="r", encoding="utf-8") as f:
                    if cls._CONF_FILE_TYPE_ == "json":
                        file_content = json.load(f)
                    if cls._CONF_FILE_TYPE_ == "yaml" or cls._CONF_FILE_TYPE_ == "yml":
                        file_content = yaml.load(f, Loader=yaml.FullLoader)
                if not isinstance(file_content, dict):
                    continue
                return str(file_content.get(key)) if file_content.get(key) else None
            except OSError:
                continue

    @classmethod
    def get_str(cls, key: str) -> Optional[str]:
        val: str
        val = cls._EXPLICIT_SETS_.get(key)
        if val:
            return val
        val = cls._get_by_env_(key)
        if val:
            return val
        val = cls._get_by_cli_(key)
        if val:
            return val
        val = cls._get_by_file_(key)
        if val:
            return val
        val = cls._DEFAULTS_.get(key)
        if val:
            return val
        return None


if __name__ == "__main__":
    pass
