import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_product

from hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidue import run, _should_run

class_path = 'hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidue'
fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/aboveGroundCropResidue"


class TestAboveGroundCropResidue(unittest.TestCase):
    @patch(f"{class_path}._is_term_type_incomplete", return_value=True)
    def test_should_run(self, _m):
        cycle = {'products': []}

        # no products => no run
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # product with total crop residue => run
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, True)

    @patch(f"{class_path}._new_product", side_effect=fake_new_product)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        print(json.dumps(value, indent=2))
        self.assertEqual(value, expected)
