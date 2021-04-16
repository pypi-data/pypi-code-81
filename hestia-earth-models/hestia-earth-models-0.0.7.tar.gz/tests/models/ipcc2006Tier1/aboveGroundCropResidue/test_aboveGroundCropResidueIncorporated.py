import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidue.aboveGroundCropResidueIncorporated import TERM_ID, \
    run, should_run

fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/aboveGroundCropResidue/{TERM_ID}"


class TestAboveGroundCropResidueIncorporated(unittest.TestCase):
    def test_should_run(self):
        self.assertEqual(should_run(), True)

    def test_run(self):
        # data on total crop residue, product and incorporated % => run
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        primary_product = cycle.get('products')[0]
        total_value = cycle.get('products')[1].get('value')[0]
        self.assertEqual(run(cycle, primary_product, total_value, 0.1), 296.57372000000004)
