import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path

from hestia_earth.models.spatial.ecoregion import _should_run, run

class_path = 'hestia_earth.models.spatial.ecoregion'
fixtures_folder = f"{fixtures_path}/spatial/ecoregion"


class TestEcoregion(unittest.TestCase):
    @patch(f"{class_path}.has_geospatial_data")
    def test_should_run(self, mock_has_geospatial_data):
        mock_has_geospatial_data.return_value = True
        self.assertEqual(_should_run({}), True)

        mock_has_geospatial_data.return_value = False
        self.assertEqual(_should_run({}), False)

    def test_run_boundary(self):
        with open(f"{fixtures_path}/spatial/boundary.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.txt", encoding='utf-8') as f:
            expected = f.read().strip()

        result = run(site)
        self.assertEqual(result, expected)

    def test_run_coordinates(self):
        with open(f"{fixtures_path}/spatial/coordinates.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.txt", encoding='utf-8') as f:
            expected = f.read().strip()

        result = run(site)
        self.assertEqual(result, expected)

    def test_run_gadm(self):
        with open(f"{fixtures_path}/spatial/gadm.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.txt", encoding='utf-8') as f:
            expected = f.read().strip()

        result = run(site)
        self.assertEqual(result, expected)
