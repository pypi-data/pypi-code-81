import unittest

from tracklr.main import TracklrApp
from tracklr.pdf import Pdf


class TestPDFCommand(unittest.TestCase):
    def test_pdf(self):
        app = TracklrApp()
        pdf = Pdf(app, None)
