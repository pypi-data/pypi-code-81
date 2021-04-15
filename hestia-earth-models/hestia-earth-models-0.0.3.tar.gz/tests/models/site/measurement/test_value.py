import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.site.measurement.value import run, _should_run


fixtures_folder = f"{fixtures_path}/site/measurement/value"


class TestMeasurementValue(unittest.TestCase):
    def test_should_run(self):
        measurement = {}

        # without min/max => NO run
        self.assertEqual(_should_run(measurement), False)

        # with min and max and value => NO run
        measurement = {
            'min': [5],
            'max': [50],
            'value': [25]
        }
        self.assertEqual(_should_run(measurement), False)

        # with min and max but not value => run
        measurement = {
            'min': [5],
            'max': [10],
            'value': []
        }
        self.assertEqual(_should_run(measurement), True)

    def test_run(self):
        with open(f"{fixtures_folder}/site.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)
