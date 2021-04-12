import sys
import unittest

from tracklr.main import main


class TestMain(unittest.TestCase):
    def test_main(self):

        test_ls = main(argv=["ls"])
