import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dspMetadataGUI.util import utils


class TestURLUtils(unittest.TestCase):
    
    def test_isURL(self):
        self.assertTrue(utils.isURL("http://www.test.org"))
        self.assertFalse(utils.isURL("not-a-url"))


if __name__ == '__main__':
    unittest.main()
