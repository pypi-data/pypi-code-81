import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.impact_assessment.organic import _should_run, run

fixtures_folder = f"{fixtures_path}/impact_assessment/organic"


class TestOrganic(unittest.TestCase):
    def test_should_run(self):
        # no cycle => no run
        impact = {}
        self.assertEqual(_should_run(impact), False)

        # with cycle no practices => no run
        cycle = {'practices': []}
        impact['cycle'] = cycle
        self.assertEqual(_should_run(impact), False)

        # with practices
        practice = {}
        cycle['practices'].append(practice)
        self.assertEqual(_should_run(impact), True)

    def test_run(self):
        with open(f"{fixtures_folder}/impact-assessment.jsonld", encoding='utf-8') as f:
            impact = json.load(f)

        value = run(impact)
        self.assertEqual(value, True)
