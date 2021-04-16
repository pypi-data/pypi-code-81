import unittest
from unittest.mock import patch
from hestia_earth.schema import SchemaType
from tests.utils import CYCLE, SITE

from hestia_earth.models.impact_assessment.pre_checks.cycle import run, _should_run

class_path = 'hestia_earth.models.impact_assessment.pre_checks.cycle'


def fake_load_calculated_node(node, type):
    return {**CYCLE} if type == SchemaType.CYCLE else {**SITE}


class TestPreCycle(unittest.TestCase):
    def test_should_run(self):
        cycle = {}
        impact = {'cycle': cycle}

        # cycle has no @id => no run
        self.assertEqual(_should_run(impact), False)
        cycle['@id'] = 'id'

        # cycle has an @id => run
        self.assertEqual(_should_run(impact), True)

    @patch(f"{class_path}._load_calculated_node", side_effect=fake_load_calculated_node)
    def test_run(self, _m):
        impact = {'cycle': {'@id': CYCLE['@id']}}

        value = run(impact)
        # loads the cycle and the site
        self.assertEqual(value['cycle'], {**CYCLE, 'site': SITE})
