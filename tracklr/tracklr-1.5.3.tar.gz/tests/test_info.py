import unittest

from tracklr.main import TracklrApp
from tracklr.info import Info


class TestPDFCommand(unittest.TestCase):
    def test_info(self):
        app = TracklrApp()
        info = Info(app, None)
