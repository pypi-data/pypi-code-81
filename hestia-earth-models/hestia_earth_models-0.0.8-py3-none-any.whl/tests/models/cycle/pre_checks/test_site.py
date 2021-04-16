import unittest
from unittest.mock import patch
from tests.utils import SITE

from hestia_earth.models.cycle.pre_checks.site import run, _should_run

class_path = 'hestia_earth.models.cycle.pre_checks.site'


class TestPreCycle(unittest.TestCase):
    def test_should_run(self):
        site = {}
        impact = {'site': site}

        # site has no @id => no run
        self.assertEqual(_should_run(impact), False)
        site['@id'] = 'id'

        # site has an @id => run
        self.assertEqual(_should_run(impact), True)

    @patch(f"{class_path}._load_calculated_node", return_value=SITE)
    def test_run(self, _m):
        cycle = {'site': {'@id': SITE['@id']}}

        value = run(cycle)
        self.assertEqual(value['site'], SITE)
