import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.ipcc2006Tier1.residue.residueBurnt import run

fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/residue"


class TestAboveGroundCropResidueBurnt(unittest.TestCase):
    def test_run(self):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        primary_product = cycle.get('products')[0]
        self.assertEqual(run(cycle, primary_product), 28.000000000000004)
