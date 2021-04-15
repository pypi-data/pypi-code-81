import unittest

from test.test_utils import make_test_atlas


class TestUnaryScalarOp(unittest.TestCase):

    def setUp(self) -> None:
        self.atlas = make_test_atlas()
        self.test_col = self.atlas.lusid_logs_apprequest.get_class()().duration
        self.test_bool = self.test_col > 1000

    def test_not_expression(self):
        not_expr = ~self.test_bool
        self.assertEqual(not_expr.get_sql(), f"not ({self.test_bool.get_sql()})")
        self.assertEqual(len(not_expr.get_lineage()), 1)

    def test_is_null_expression(self):
        is_null_expr = self.test_col.is_null()
        self.assertEqual(is_null_expr.get_sql(), f"{self.test_col.get_sql()} is null")
        self.assertEqual(len(is_null_expr.get_lineage()), 1)

    def test_negative_expression(self):
        neg_expr = -self.test_col
        self.assertEqual(neg_expr.get_sql(), f"-{self.test_col.get_sql()}")
        self.assertEqual(len(neg_expr.get_lineage()), 1)
