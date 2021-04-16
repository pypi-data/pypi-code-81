import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_input

from hestia_earth.models.faostat2018.seed import TERM_ID, _should_run, run

class_path = 'hestia_earth.models.faostat2018.seed'
fixtures_folder = f"{fixtures_path}/faostat2018/{TERM_ID}"


class TestSeed(unittest.TestCase):
    @patch(f"{class_path}._is_term_type_incomplete", return_value=True)
    def test_should_run(self, mock_is_term_type_incomplete):
        mock_is_term_type_incomplete.return_value = True
        self.assertEqual(_should_run({}), True)

        mock_is_term_type_incomplete.return_value = False
        self.assertEqual(_should_run({}), False)

    @patch(f"{class_path}._new_input", side_effect=fake_new_input)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(cycle)
        self.assertEqual(result, expected)
