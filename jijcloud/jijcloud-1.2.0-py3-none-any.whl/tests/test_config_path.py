import unittest
import os
from jijcloud.setting import load_config


class TestConfigPath(unittest.TestCase):
    def test_relative_path(self):
        _ = load_config('./tests/testconfig.toml')
        _ = load_config('./tests/../tests/testconfig.toml')

    def test_absolute_path(self):
        current_dir = os.getcwd()
        file_name = current_dir + '/tests/testconfig.toml'
        _ = load_config(file_name)
