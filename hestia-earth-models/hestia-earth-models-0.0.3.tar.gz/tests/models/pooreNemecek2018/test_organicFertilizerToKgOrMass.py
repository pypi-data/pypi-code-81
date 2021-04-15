import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_input

from hestia_earth.models.pooreNemecek2018.organicFertilizerToKgOrMass import run, _should_run

class_path = 'hestia_earth.models.pooreNemecek2018.organicFertilizerToKgOrMass'
fixtures_folder = f"{fixtures_path}/pooreNemecek2018/organicFertilizerToKgOrMass"


class TestOrganicFertilizerKgMass(unittest.TestCase):
    def test_should_run(self):
        # cycle with no organic fertiliser inputs
        inputs = []
        self.assertEqual(_should_run(inputs), [])

        term_id = 'manureFresh'
        # cycle with an organic fertiliser + missing as Mass data
        inputs.append({
            'term': {
                '@id': term_id + 'AsN'
            },
            'value': 0.00208
        })
        self.assertEqual(_should_run(inputs), [term_id])

        # cycle with an organic fertiliser + as mass data gap-filled old version
        inputs.append({
            'term': {
                '@id': term_id + 'KgMass'
            },
            'value': 0.4
        })
        self.assertEqual(_should_run(inputs), [term_id])

    @patch(f"{class_path}._new_input", side_effect=fake_new_input)
    def test_run(self, _m):
        # cycle with an organic fertiliser => Iranian Hazelnut example
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertCountEqual(value, expected)
