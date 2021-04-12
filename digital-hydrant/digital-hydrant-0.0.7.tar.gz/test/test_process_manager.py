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

import unittest
from unittest.mock import patch, Mock
from multiprocessing import Process
import time
import os
import schedule
from configparser import ConfigParser


from digital_hydrant.process_manager import ProcessManager
from digital_hydrant.config import update_config, ini_path

from . import stub_collectors


@patch("digital_hydrant.process_manager.ProcessManager.scheduler")
class TestProcessManager(unittest.TestCase):
    def setUp(self):
        self.manager = ProcessManager()
        self.manager.logger = Mock()
        self.original = ConfigParser()
        self.original.read(ini_path)

    def tearDown(self):
        with open(ini_path, "w") as configfile:
            self.original.write(configfile)

    def test_add_process(self, mock):
        m = Mock()
        self.manager.add_process("tester", m, ("tester",))

        self.assertEqual(1, len(self.manager.process_details))
        self.assertIn("tester", self.manager.process_details)

    def test_is_scheduled(self, mock):
        self.assertFalse(self.manager.is_scheduled("tester"))

        self.manager.jobs["tester"] = schedule.Job(1)

        self.assertTrue(self.manager.is_scheduled("tester"))
        self.assertFalse(self.manager.is_scheduled("random"))

    def test_schedule_every_5_seconds(self, mock):
        self.manager.schedule("tester", "* * * * 5")

        self.assertEqual(1, len(self.manager.jobs))
        self.assertIn("tester", self.manager.jobs)
        self.assertIsInstance(self.manager.jobs["tester"], schedule.Job)

        self.assertEqual("run_job", self.manager.jobs["tester"].job_func.__name__)
        self.assertEqual("seconds", self.manager.jobs["tester"].unit)
        self.assertEqual(5, self.manager.jobs["tester"].interval)
        self.assertIsNone(self.manager.jobs["tester"].at_time)

    def test_schedule_every_minute(self, mock):
        self.manager.schedule("tester", "* * * 1 *")

        self.assertEqual(1, len(self.manager.jobs))
        self.assertIn("tester", self.manager.jobs)
        self.assertIsInstance(self.manager.jobs["tester"], schedule.Job)

        self.assertEqual("run_job", self.manager.jobs["tester"].job_func.__name__)
        self.assertEqual("minutes", self.manager.jobs["tester"].unit)
        self.assertEqual(1, self.manager.jobs["tester"].interval)
        self.assertEqual(0, self.manager.jobs["tester"].at_time.hour)
        self.assertEqual(0, self.manager.jobs["tester"].at_time.minute)
        self.assertEqual(0, self.manager.jobs["tester"].at_time.second)

    def test_schedule_every_15_hours(self, mock):
        self.manager.schedule("tester", "* * 15 * 59")

        self.assertEqual(1, len(self.manager.jobs))
        self.assertIn("tester", self.manager.jobs)
        self.assertIsInstance(self.manager.jobs["tester"], schedule.Job)

        self.assertEqual("run_job", self.manager.jobs["tester"].job_func.__name__)
        self.assertEqual("hours", self.manager.jobs["tester"].unit)
        self.assertEqual(15, self.manager.jobs["tester"].interval)
        self.assertEqual(0, self.manager.jobs["tester"].at_time.hour)
        self.assertEqual(0, self.manager.jobs["tester"].at_time.minute)
        self.assertEqual(59, self.manager.jobs["tester"].at_time.second)

    def test_schedule_every_2_days(self, mock):
        self.manager.schedule("tester", "* 2 20 1 *")

        self.assertEqual(1, len(self.manager.jobs))
        self.assertIn("tester", self.manager.jobs)
        self.assertIsInstance(self.manager.jobs["tester"], schedule.Job)

        self.assertEqual("run_job", self.manager.jobs["tester"].job_func.__name__)
        self.assertEqual("days", self.manager.jobs["tester"].unit)
        self.assertEqual(2, self.manager.jobs["tester"].interval)
        self.assertEqual(20, self.manager.jobs["tester"].at_time.hour)
        self.assertEqual(1, self.manager.jobs["tester"].at_time.minute)
        self.assertEqual(0, self.manager.jobs["tester"].at_time.second)

    def test_schedule__on_thursday(self, mock):
        self.manager.schedule("tester", "5 * 10 19 45")

        self.assertEqual(1, len(self.manager.jobs))
        self.assertIn("tester", self.manager.jobs)
        self.assertIsInstance(self.manager.jobs["tester"], schedule.Job)

        self.assertEqual("run_job", self.manager.jobs["tester"].job_func.__name__)
        self.assertEqual("weeks", self.manager.jobs["tester"].unit)
        self.assertEqual("thursday", self.manager.jobs["tester"].start_day)
        self.assertEqual(1, self.manager.jobs["tester"].interval)
        self.assertEqual(10, self.manager.jobs["tester"].at_time.hour)
        self.assertEqual(19, self.manager.jobs["tester"].at_time.minute)
        self.assertEqual(45, self.manager.jobs["tester"].at_time.second)

    def test_schedule_default(self, mock):
        self.manager.schedule("tester", "* * * * *")

        self.assertEqual(1, len(self.manager.jobs))
        self.assertIn("tester", self.manager.jobs)
        self.assertIsInstance(self.manager.jobs["tester"], schedule.Job)

        self.assertEqual("run_job_once", self.manager.jobs["tester"].job_func.__name__)
        self.assertEqual("seconds", self.manager.jobs["tester"].unit)
        self.assertEqual(1, self.manager.jobs["tester"].interval)

    def test_check_for_new_jobs(self, mock):
        self.manager.collectors.append("newest_section")
        self.manager.check_for_new_jobs()
        start = len(self.manager.process_details)

        update_config({"newest_section": {"something_else": True}})

        self.manager.check_for_new_jobs()
        self.assertEqual(start, len(self.manager.process_details))

        update_config({"newest_section": {"enabled": True}})

        self.manager.check_for_new_jobs()
        self.assertEqual(start + 1, len(self.manager.process_details))
