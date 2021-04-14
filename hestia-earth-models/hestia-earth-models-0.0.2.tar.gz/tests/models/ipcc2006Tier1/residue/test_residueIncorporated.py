import unittest

from hestia_earth.models.ipcc2006Tier1.residue.residueIncorporated import run


class TestAboveGroundCropResidueIncorporated(unittest.TestCase):
    def test_run(self):
        self.assertEqual(run(), None)
