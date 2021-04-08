import os
import unittest
import json
import logging
from kinnaird_utils.files import read_yaml_file

logger = logging.getLogger(__name__)


class FileTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.example_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "files",
            "example.yml"
        ))

    def test_read_yaml_file(self):
        results = read_yaml_file(self.example_file)
        print(json.dumps(results, indent=4))
        expected_results = {
            "first_name": "Kinnaird",
            "last_name": "McQuade"
        }
        self.assertDictEqual(results, expected_results)