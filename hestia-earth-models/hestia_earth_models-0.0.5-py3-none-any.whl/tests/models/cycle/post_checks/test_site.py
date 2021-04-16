import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.post_checks.site import run, _should_run


class TestPostCycle(unittest.TestCase):
    def test_should_run(self):
        site = {}
        impact = {'site': site}

        # site has no @id => no run
        self.assertEqual(_should_run(impact), False)
        site['@id'] = 'id'

        # site has an id => run
        self.assertEqual(_should_run(impact), True)

    def test_run(self):
        # contains a full site
        with open(f"{fixtures_path}/cycle/complete.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        site = cycle.get('site')
        value = run(cycle)
        self.assertEqual(value['site'], {'@type': site['@type'], '@id': site['@id']})
