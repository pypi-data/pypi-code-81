import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.impact_assessment.product import _should_run, run

fixtures_folder = f"{fixtures_path}/impact_assessment/product"


class TestPrimaryProduct(unittest.TestCase):
    def test_should_run(self):
        # no cycle => no run
        impact = {}
        self.assertEqual(_should_run(impact), False)

        # with cycle no primary products => no run
        cycle = {'products': []}
        impact['cycle'] = cycle
        self.assertEqual(_should_run(impact), False)

        # with primary product
        product = {'primary': True}
        cycle['products'].append(product)
        self.assertEqual(_should_run(impact), True)

    def test_run(self):
        with open(f"{fixtures_folder}/impact-assessment.jsonld", encoding='utf-8') as f:
            impact = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(impact)
        self.assertEqual(value, expected)
