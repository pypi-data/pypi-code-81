import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_download_term

from hestia_earth.models.spatial.region import _should_run, run

class_path = 'hestia_earth.models.spatial.region'
fixtures_folder = f"{fixtures_path}/spatial/region"


class TestRegion(unittest.TestCase):
    @patch(f"{class_path}.has_geospatial_data")
    def test_should_run(self, mock_has_geospatial_data):
        mock_has_geospatial_data.return_value = True
        self.assertEqual(_should_run({}), True)

        mock_has_geospatial_data.return_value = False
        self.assertEqual(_should_run({}), False)

    @patch(f"{class_path}.download_hestia", side_effect=fake_download_term)
    def test_run(self, _m):
        with open(f"{fixtures_path}/spatial/coordinates.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)
