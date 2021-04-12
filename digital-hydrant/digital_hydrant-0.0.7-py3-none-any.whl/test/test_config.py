# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import os
import unittest
from configparser import ConfigParser


from digital_hydrant.config import config as conf, ini_path
from digital_hydrant.config import get_sections, update_config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.original = ConfigParser()
        self.original.read(ini_path)

    def tearDown(self):
        with open(ini_path, "w") as configfile:
            self.original.write(configfile)

    def test_base_config(self):
        sections = conf.sections()

        self.assertIn("global", sections)
        self.assertIn("api", sections)

    def test_get_sections(self):
        conf["random"] = {"question": "Who?"}

        sections = get_sections("ran")

        self.assertIn("random", sections)

    def test_get_sections_no_match(self):
        sections = get_sections("zzzzzzzz")

        self.assertEqual(0, len(sections))

    def test_update_config(self):
        update_config({"api": {"token": "the wrong one"}})

        self.assertTrue(check_if_string_in_file("the wrong one"))

    def test_update_config_new_section(self):
        update_config({"newSection": {"wrong": "invalid"}})

        self.assertTrue(check_if_string_in_file("newSection"))

    def test_update_config_invalid_dict(self):
        update_config({"bad": "lame"})

        self.assertFalse(check_if_string_in_file("bad"))

    def test_update_config_no_new_values(self):
        self.assertIn("logging", conf.sections())
        self.assertIn("level", conf.options("logging"))
        self.assertEqual("INFO", conf.get("logging", "level"))

        update_config(
            {"randomSection": {"hello": "world", "logging": {"level": "ERROR"}}}, False
        )

        self.assertTrue(check_if_string_in_file("randomSection"))
        self.assertTrue(check_if_string_in_file("hello = world"))
        self.assertFalse(check_if_string_in_file("level = ERROR"))


def check_if_string_in_file(string_to_search):
    with open(ini_path, "r") as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False
