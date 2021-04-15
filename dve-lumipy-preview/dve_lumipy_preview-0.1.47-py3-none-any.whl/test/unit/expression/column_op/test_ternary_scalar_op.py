import unittest

from test.test_utils import make_test_atlas


class TestTernaryScalarOp(unittest.TestCase):

    def setUp(self) -> None:
        self.atlas = make_test_atlas()
        self.test_col = self.atlas.lusid_logs_apprequest.get_class()().duration

    def test_ternary_ops(self):
        between = self.test_col.between(0, 1)
        self.assertEqual(len(between.get_lineage()), 3)
        self.assertEqual(f'{self.test_col.get_sql()} between 0 and 1', between.get_sql())

        not_between = self.test_col.not_between(0, 1)
        self.assertEqual(len(between.get_lineage()), 3)
        self.assertEqual(f'{self.test_col.get_sql()} not between 0 and 1', not_between.get_sql())
