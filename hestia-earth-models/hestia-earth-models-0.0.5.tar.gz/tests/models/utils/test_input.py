import unittest
from unittest.mock import patch
from tests.utils import TERM

from hestia_earth.models.utils.input import _new_input


class TestInput(unittest.TestCase):
    @patch('hestia_earth.models.utils.input.download_hestia', return_value=TERM)
    def test_new_input(self, _m):
        # with a Term as string
        input = _new_input('term')
        self.assertEqual(input, {
            '@type': 'Input',
            'term': TERM
        })

        # with a Term as dict
        input = _new_input(TERM)
        self.assertEqual(input, {
            '@type': 'Input',
            'term': TERM
        })
