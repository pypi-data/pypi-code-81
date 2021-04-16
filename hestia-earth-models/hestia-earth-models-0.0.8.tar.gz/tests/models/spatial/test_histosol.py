import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.spatial.histosol import TERM_ID, _should_run, run

class_path = 'hestia_earth.models.spatial.histosol'
fixtures_folder = f"{fixtures_path}/spatial/{TERM_ID}"


class TestHistosol(unittest.TestCase):
    @patch(f"{class_path}.has_geospatial_data", return_value=True)
    def test_should_run(self, _m):
        # with no soilType => run
        site = {'measurements': []}
        self.assertEqual(_should_run(site), True)

        # with an existing soilType => NO run
        with open(f"{fixtures_folder}/with-soilType.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        self.assertEqual(_should_run(site), False)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_coordinates(self, _m):
        with open(f"{fixtures_folder}/coordinates.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_boundary(self, _m):
        with open(f"{fixtures_folder}/boundary.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_gadm(self, _m):
        with open(f"{fixtures_path}/spatial/gadm.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        result = run(site)
        self.assertEqual(result, [])
