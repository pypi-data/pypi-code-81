import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.pre_checks.startDate import run, _should_run

fixtures_folder = f"{fixtures_path}/cycle/pre_checks/startDate"


class TestStartDate(unittest.TestCase):
    def test_should_run(self):
        cycle = {}

        # no endDate => no gap-fill
        cycle['endDate'] = None
        self.assertEqual(_should_run(cycle), False)

        cycle['endDate'] = '2010'
        # no cycleDuration => no gap-fill
        cycle['cycleDuration'] = None
        self.assertEqual(_should_run(cycle), False)

        cycle['cycleDuration'] = 120
        # with a startDate => no gap-fill
        cycle['startDate'] = '2010'
        self.assertEqual(_should_run(cycle), False)

        cycle['startDate'] = None
        # endDate not precise enough => no gap-fill
        cycle['endDate'] = '2020-01'
        self.assertEqual(_should_run(cycle), False)

        # endDate is precise enough => gap-fill
        cycle['endDate'] = '2020-01-01'
        self.assertEqual(_should_run(cycle), True)

    def test_run(self):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
