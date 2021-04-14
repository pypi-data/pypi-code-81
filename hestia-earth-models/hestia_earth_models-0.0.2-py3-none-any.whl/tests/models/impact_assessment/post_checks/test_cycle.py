import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.impact_assessment.post_checks.cycle import run, _should_run


class TestPostCycle(unittest.TestCase):
    def test_should_run(self):
        cycle = {}
        impact = {'cycle': cycle}

        # cycle has no @id => no run
        self.assertEqual(_should_run(impact), False)
        cycle['@id'] = 'id'

        # cycle has an id => run
        self.assertEqual(_should_run(impact), True)

    def test_run(self):
        # contains a full cycle
        with open(f"{fixtures_path}/impact_assessment/complete.jsonld", encoding='utf-8') as f:
            impact = json.load(f)

        cycle = impact.get('cycle')
        value = run(impact)
        self.assertEqual(value['cycle'], {'@type': cycle['@type'], '@id': cycle['@id']})
