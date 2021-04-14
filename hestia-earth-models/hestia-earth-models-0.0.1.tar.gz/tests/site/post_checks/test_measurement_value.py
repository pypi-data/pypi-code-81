import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.site.post_checks.measurement_value import _should_run, run


fixtures_folder = f"{fixtures_path}/site/post_checks/measurement-value"


class TestMeasurementValue(unittest.TestCase):
    def test_should_run(self):
        site = {}

        # no measurements => NO gap-fill
        self.assertEqual(_should_run(site), (False, []))

        # measurements without value/min/max => NO gap-fill
        site['measurements'] = [{}]
        self.assertEqual(_should_run(site), (False, []))

        # measurements without min/max => NO gap-fill
        site['measurements'] = [{
            'value': []
        }]
        self.assertEqual(_should_run(site), (False, []))

        # with min and max and value => NO gap-fill
        site['measurements'] = [{
            'min': [5],
            'max': [50],
            'value': [25]
        }]
        self.assertEqual(_should_run(site), (False, []))

        # with min and max but not value => gap-fill
        site['measurements'] = [{
            'min': [5],
            'max': [10],
            'value': []
        }]
        (should_run, measurements) = _should_run(site)
        self.assertEqual(should_run, True)
        self.assertEqual(measurements, site['measurements'])

    def test_run(self):
        with open(f"{fixtures_folder}/site.jsonld", encoding='utf-8') as f:
            site = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        result = run(site)
        self.assertEqual(result, expected)
