import unittest
import logging
from kinnaird_utils.text import strip_special_characters

logger = logging.getLogger(__name__)


def get_input(text):
    return input(text)


def answer():
    ans = get_input('enter yes or no')
    if ans == 'yes':
        return 'you entered yes'
    if ans == 'no':
        return 'you entered no'


class TextTestCase(unittest.TestCase):
    def test_strip_special_characters(self):
        input_string = "Special $#! characters   spaces 888323"
        result = strip_special_characters(input_string)
        expected_output = "Specialcharactersspaces888323"
        self.assertEqual(result, expected_output)
