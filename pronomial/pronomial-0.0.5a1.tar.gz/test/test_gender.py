import unittest
from pronomial.utils import predict_gender


class TestNameGender(unittest.TestCase):
    def test_female(self):
        self.assertEqual(predict_gender("Elsa"),  "female")
        self.assertEqual(predict_gender("Sarah"),  "female")
        self.assertEqual(predict_gender("Inês"),  "female")
        self.assertEqual(predict_gender("Joana"),  "female")
        self.assertEqual(predict_gender("Maria"),  "female")

    def test_male(self):
        self.assertEqual(predict_gender("Jake"),  "male")
        self.assertEqual(predict_gender("Bob"),  "male")
        self.assertEqual(predict_gender("Guy"),  "male")
        self.assertEqual(predict_gender("Daniel"),  "male")
        self.assertEqual(predict_gender("Kevin"),  "male")
        self.assertEqual(predict_gender("João"),  "male")
