import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_property

from hestia_earth.models.ipcc2019Tier1.nitrogenContent import TERM_ID, _should_run, _should_run_product, run

class_path = 'hestia_earth.models.ipcc2019Tier1.nitrogenContent'
fixtures_folder = f"{fixtures_path}/ipcc2019Tier1/{TERM_ID}"


class TestNitrogenContent(unittest.TestCase):
    def test_should_run(self):
        cycle = {'products': []}

        # no products => no run
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with primary product => no run
        cycle['products'] = [{'primary': True}]
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with related product => run
        cycle['products'].append({'term': {'@id': 'belowGroundCropResidue'}})
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, True)

    def test_should_run_product(self):
        product = {}

        # not a runed product => no run
        product['term'] = {'@id': 'random id'}
        self.assertEqual(_should_run_product(product), False)

        # with a runed product => run
        product['term']['@id'] = 'aboveGroundCropResidueTotal'
        self.assertEqual(_should_run_product(product), True)

        prop = {
            'term': {
                '@id': TERM_ID
            }
        }
        product['properties'] = [prop]
        self.assertEqual(_should_run_product(product), False)

    @patch(f"{class_path}._new_property", side_effect=fake_new_property)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
