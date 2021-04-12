import pytest
import unittest

from tracklr import Tracklr


class TestTracklr(unittest.TestCase):
    def setUp(self):

        self.tracklr = Tracklr()
        self.config = "tests/tracklr.yml"
        self.tracklr.__config__ = open(self.config, "r").read()
        self.tracklr.configure()

    def test_init(self):

        self.assertIn("tests/vdir_storage", self.tracklr.__config__)

    def test_loadrc(self):

        self.tracklr.loadrc(self.config)
        self.assertEqual(self.config, self.tracklr.loaded_config_file)
        self.assertEqual(
            self.tracklr.config,
            {"calendars": [
                {"location": "tests/vdir_storage"},
                {"name": "test",
                 "subtitle": "My Test Subtitle",
                 "location": "tests/vdir_storage"}]}
        )

    def test_configure(self):

        self.assertEqual(
            self.tracklr.config,
            {"calendars": [
                {"location": "tests/vdir_storage"},
                {"name": "test",
                 "subtitle": "My Test Subtitle",
                 "location": "tests/vdir_storage"}]}
        )

    def test_get_calendar_config(self):

        config = self.tracklr.get_calendar_config(None)
        self.assertEqual(config, {'name': 'default', 'location': 'tests/vdir_storage'})

        with pytest.raises(Exception):
            assert self.tracklr.get_calendar_config("404")

    def test_get_title(self):

        cal = self.tracklr.get_calendar_config("default")
        self.tracklr.get_feed(cal["name"], cal["location"])

        title = self.tracklr.get_title("default", None)
        self.assertEqual(title, "Test Displayname")

        title = self.tracklr.get_title("default", "My Custom Title")
        self.assertEqual(title, "My Custom Title")

        cal = self.tracklr.get_calendar_config("test")
        self.tracklr.get_feed(cal["name"], cal["location"])

        title = self.tracklr.get_title("test", None)
        self.assertEqual(title, "Test Displayname")

        title = self.tracklr.get_title("test", "My New Title")
        self.assertEqual(title, "My New Title")

    def test_get_subtitle(self):

        cal = self.tracklr.get_calendar_config("default")
        self.tracklr.get_feed(cal["name"], cal["location"])

        title = self.tracklr.get_subtitle("default", None)
        self.assertEqual(title, "Command-line Productivity Toolset")

        title = self.tracklr.get_subtitle("default", "My Subtitle")
        self.assertEqual(title, "My Subtitle")

        cal = self.tracklr.get_calendar_config("test")
        self.tracklr.get_feed(cal["name"], cal["location"])

        title = self.tracklr.get_subtitle("test", None)
        self.assertEqual(title, "My Test Subtitle")

        title = self.tracklr.get_subtitle("test", "My Subtitle")
        self.assertEqual(title, "My Subtitle")

    def test_get_titles(self):

        cal = self.tracklr.get_calendar_config("default")
        self.tracklr.get_feed(cal["name"], cal["location"])

        titles = self.tracklr.get_titles("default", None, None)
        self.assertEqual(titles, "Test Displayname - Command-line Productivity Toolset")

        titles = self.tracklr.get_titles("default", "A", "B")
        self.assertEqual(titles, "A - B")

        cal = self.tracklr.get_calendar_config("test")
        self.tracklr.get_feed(cal["name"], cal["location"])

        titles = self.tracklr.get_titles("test", None, None)
        self.assertEqual(titles, "Test Displayname - My Test Subtitle")

        titles = self.tracklr.get_titles("test", "C", "D")
        self.assertEqual(titles, "C - D")

    def test_report(self):

        report = self.tracklr.get_report(None, "test", None, None, None)

    def test_banner(self):

        banner = self.tracklr.banner("default", use_figlet=True)

        self.assertIn(f" v{self.tracklr.__version__}", banner)
