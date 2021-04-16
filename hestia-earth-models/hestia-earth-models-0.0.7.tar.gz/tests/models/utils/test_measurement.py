import unittest
from unittest.mock import patch
from tests.utils import TERM, SOURCE

from hestia_earth.models.utils.measurement import _new_measurement


class TestInput(unittest.TestCase):
    @patch('hestia_earth.models.utils.measurement.find_node_exact', return_value=SOURCE)
    @patch('hestia_earth.models.utils.measurement.download_hestia', return_value=TERM)
    def test_new_measurement(self, _m1, _m2):
        # with a Term as string
        measurement = _new_measurement('term')
        self.assertEqual(measurement, {
            '@type': 'Measurement',
            'term': TERM
        })

        # with a Term as dict
        measurement = _new_measurement(TERM)
        self.assertEqual(measurement, {
            '@type': 'Measurement',
            'term': TERM
        })

        # with a title
        title = 'title'
        self.assertEqual(_new_measurement(TERM, title), {
            '@type': 'Measurement',
            'term': TERM,
            'source': SOURCE
        })
