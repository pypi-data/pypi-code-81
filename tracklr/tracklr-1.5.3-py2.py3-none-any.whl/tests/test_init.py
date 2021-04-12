import unittest

from tracklr.main import TracklrApp
from tracklr.init import Init


class TestPDFCommand(unittest.TestCase):
    def test_init(self):
        app = TracklrApp()
        init = Init(app, None)
