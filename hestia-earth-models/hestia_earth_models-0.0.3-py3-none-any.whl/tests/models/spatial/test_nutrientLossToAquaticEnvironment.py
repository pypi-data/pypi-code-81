import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.spatial.nutrientLossToAquaticEnvironment import _should_run, TERM_ID, run

class_path = 'hestia_earth.models.spatial.nutrientLossToAquaticEnvironment'
fixtures_folder = f"{fixtures_path}/spatial/{TERM_ID}"


class TestNutrientLossAquaticEnvironment(unittest.TestCase):
    @patch(f"{class_path}.has_geospatial_data")
    def test_should_run(self, mock_has_geospatial_data):
        mock_has_geospatial_data.return_value = True
        self.assertEqual(_should_run({}), True)

        mock_has_geospatial_data.return_value = False
        self.assertEqual(_should_run({}), False)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_coordinates(self, _m):
        with open(f"{fixtures_path}/spatial/coordinates.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_boundary(self, _m):
        with open(f"{fixtures_path}/spatial/boundary.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_gadm(self, _m):
        with open(f"{fixtures_path}/spatial/gadm.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/gadm/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)
