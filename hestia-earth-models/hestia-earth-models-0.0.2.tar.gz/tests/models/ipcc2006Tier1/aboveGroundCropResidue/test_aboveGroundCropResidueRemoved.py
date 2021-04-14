import unittest
from tests.utils import fixtures_path

from hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidue.aboveGroundCropResidueRemoved import TERM_ID, \
    run, should_run

fixtures_folder = f"{fixtures_path}/ipcc2006Tier1/aboveGroundCropResidue/{TERM_ID}"


class TestAboveGroundCropResidueRemoved(unittest.TestCase):
    def test_should_run(self):
        cycle = {}

        # no primary product => no run
        self.assertEqual(should_run(cycle, None), False)

        # with primary product => run
        self.assertEqual(should_run(cycle, {}), True)

    def test_run(self):
        total_value = 120
        self.assertEqual(run(None, None, total_value, 0.5), 60)
