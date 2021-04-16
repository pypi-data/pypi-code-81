import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.spatial.clayContent import TERM_IDS, _should_run, _run_single, run

class_path = 'hestia_earth.models.spatial.clayContent'
fixtures_folder = f"{fixtures_path}/spatial/clayContent"


class TestClayContent(unittest.TestCase):
    @patch(f"{class_path}.has_geospatial_data")
    def test_should_run(self, mock_has_geospatial_data):
        mock_has_geospatial_data.return_value = True

        site = {}
        # with 1 measurement with model => run
        measurement = {
            'term': {
                '@id': list(TERM_IDS.keys())[0]
            }
        }
        site['measurements'] = [measurement]
        should_run, *args = _should_run(site)
        self.assertEqual(should_run, True)

        # with 3 measurements with model => NO run
        site['measurements'].append({
            'term': {
                '@id': list(TERM_IDS.keys())[1]
            }
        })
        site['measurements'].append({
            'term': {
                '@id': list(TERM_IDS.keys())[2]
            }
        })
        should_run, *args = _should_run(site)
        self.assertEqual(should_run, False)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_single(self, _m1):
        model = list(TERM_IDS.keys())[0]
        measurements = [{
            'term': {
                '@id': list(TERM_IDS.keys())[1]
            },
            'value': [20]
        }, {
            'term': {
                '@id': list(TERM_IDS.keys())[2]
            },
            'value': [30]
        }]
        measurement = _run_single(measurements, model)[0]
        self.assertEqual(measurement.get('value'), [50])

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_coordinates(self, _m1):
        with open(f"{fixtures_path}/spatial/coordinates.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_boundary(self, _m1):
        with open(f"{fixtures_path}/spatial/boundary.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)

    @patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
    def test_run_gadm(self, _m1):
        with open(f"{fixtures_path}/spatial/gadm.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/gadm/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)
