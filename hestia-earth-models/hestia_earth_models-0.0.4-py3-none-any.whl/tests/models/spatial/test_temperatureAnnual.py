import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.spatial.temperatureAnnual import TERM_ID, _should_run, run

class_path = 'hestia_earth.models.spatial.temperatureAnnual'
fixtures_folder = f"{fixtures_path}/spatial/{TERM_ID}"


def fake_cycles(*args): return [{'@id': 'id', 'endDate': '2009'}]


class TestTemperatureAnnual(unittest.TestCase):
    @patch(f"{class_path}.has_geospatial_data")
    def test_should_run(self, mock_has_geospatial_data):
        mock_has_geospatial_data.return_value = True

        site = {}
        end_year = 1978

        # end date too far => NO run
        self.assertEqual(_should_run(site, end_year), False)

        # end date not too far => run
        end_year = 1990
        self.assertEqual(_should_run(site, end_year), True)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    @patch(f"{class_path}._related_cycles", side_effect=fake_cycles)
    def test_run_coordinates(self, _m1, _m2):
        with open(f"{fixtures_path}/spatial/coordinates.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    @patch(f"{class_path}._related_cycles", side_effect=fake_cycles)
    def test_run_boundary(self, _m1, _m2):
        with open(f"{fixtures_path}/spatial/boundary.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/boundary/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    @patch(f"{class_path}._related_cycles", side_effect=fake_cycles)
    def test_run_gadm(self, _m1, _m2):
        with open(f"{fixtures_path}/spatial/gadm.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/gadm/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)
