import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.akagiEtAl2011AndIpcc2006.nh3ToAirCropResidueBurning import TERM_ID, run, _should_run, PRODUCT

class_path = f"hestia_earth.models.akagiEtAl2011AndIpcc2006.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/akagiEtAl2011AndIpcc2006/{TERM_ID}"


class TestNh3ToAirCropResidueBurning(unittest.TestCase):
    @patch(f"{class_path}._is_term_type_complete", return_value=False)
    def test_should_run(self, mock_is_term_type_complete):
        # no products => no run
        cycle = {'products': []}
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # with correct product but no value => no run
        cycle = {'products': [{
            'term': {'@id': PRODUCT},
            'value': []
        }]}
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, False)

        # complete data
        mock_is_term_type_complete.return_value = True
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, True)

        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)
        should_run, *args = _should_run(cycle)
        self.assertEqual(should_run, True)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)

    @patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
    def test_run_data_complete(self, _m):
        with open(f"{fixtures_folder}/no-product-data-complete/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/no-product-data-complete/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
