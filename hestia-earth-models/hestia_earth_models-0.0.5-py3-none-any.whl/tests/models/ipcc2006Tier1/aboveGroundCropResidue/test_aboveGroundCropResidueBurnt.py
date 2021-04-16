import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidue.aboveGroundCropResidueBurnt import TERM_ID, \
    run, should_run

fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/aboveGroundCropResidue/{TERM_ID}"


class TestAboveGroundCropResidueBurnt(unittest.TestCase):
    def test_should_run(self):
        cycle = {}

        # no primary product => no run
        self.assertEqual(should_run(cycle, None), False)

        # with primary product => run
        self.assertEqual(should_run(cycle, {}), True)

    def test_run(self):
        # data on total crop residue, product and burnt practice amount => run
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        primary_product = cycle.get('products')[0]
        total_value = cycle.get('products')[1].get('value')[0]
        self.assertEqual(run(cycle, primary_product, total_value, 0.5), 1334.58174)

    def test_run_with_removed_data(self):
        # data on total crop residue, residue removed, product and burnt practice amount => run
        with open(f"{fixtures_folder}/removed-data/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        primary_product = cycle.get('products')[0]
        total_value = cycle.get('products')[1].get('value')[0]
        self.assertEqual(run(cycle, primary_product, total_value, 0.5), 434.25)
