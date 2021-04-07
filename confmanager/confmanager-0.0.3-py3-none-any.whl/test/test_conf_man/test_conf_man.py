# -*- coding:utf-8 -*-
# @Author   : Haogooder
# @Date     : 2021/4/7 4月 07 2021
# @Software : PyCharm
# @FileName : test_conf_man
# @Desc     : The description of this file
import os
import sys

from conf_man import ConfMan


class TestConfMan:
    def test_set(self):
        ConfMan.clear()
        ConfMan.set("k", "v")
        val = ConfMan.get_str("k")
        assert val == "v"

    def test_env(self):
        ConfMan.clear()
        ConfMan.set_env_prefix("my")
        ConfMan.bind_env("k", "envkey")
        val = ConfMan.get_str("k")
        assert val is None
        os.environ.update({"MY_ENVKEY": "v"})
        val = ConfMan.get_str("k")
        assert val == "v"

    def test_flag(self):
        ConfMan.clear()
        ConfMan.bind_flag("k", "flagkey")
        val = ConfMan.get_str("k")
        assert val is None
        sys.argv.append("--flagkey")
        sys.argv.append("v")
        val = ConfMan.get_str("k")
        assert val == "v"

    def test_file(self):
        ConfMan.clear()
        ConfMan.add_conf_dir(os.path.dirname(__file__))
        ConfMan.set_conf_file_name("config.json")
        ConfMan.set_conf_file_type("json")
        val = ConfMan.get_str("k")
        assert val == "v1"

        ConfMan.clear()
        ConfMan.add_conf_dir(os.path.dirname(__file__))
        ConfMan.set_conf_file_name("config.yaml")
        ConfMan.set_conf_file_type("yaml")
        val = ConfMan.get_str("k")
        assert val == "v2"


if __name__ == "__main__":
    pass
