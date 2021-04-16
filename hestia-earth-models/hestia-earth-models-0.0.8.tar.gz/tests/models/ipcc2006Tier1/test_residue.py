import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_practice

from hestia_earth.models.ipcc2006Tier1.residue import run, _should_run_model

class_path = 'hestia_earth.models.ipcc2006Tier1.residue'
fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/residue"


class TestAboveGroundCropResiduePractices(unittest.TestCase):
    def test_should_run_model(self):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        term_id = cycle['practices'][0]['term']['@id']
        self.assertEqual(_should_run_model(term_id, cycle), False)

        term_id = 'random term'
        self.assertEqual(_should_run_model(term_id, cycle), True)

    @patch(f"{class_path}._new_practice", side_effect=fake_new_practice)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
