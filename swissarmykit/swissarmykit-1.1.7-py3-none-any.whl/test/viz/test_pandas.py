from unittest import TestCase

from numpy import NaN
from swissarmykit.viz.Pandas import Pandas


class TestPandas(TestCase):

    def setUp(self) -> None:
        pass

    def test_isnull(self):
        self.fail()

    def test_notnull(self):
        self.fail()

    def test_transpose(self):
        self.fail()

    def test_fill_nan(self):
        data = [[1, 'a', NaN], [2, 'b'], [4, NaN, 'd'], [4, 'a', 4], [4, 'f', NaN], [3, NaN, NaN] ]
        p = Pandas(data)
        p.fill_nan(0, [1,2])
        print(p)


    def test_sort_by_index(self):
        self.fail()

    def test_sort_by_values(self):
        self.fail()

    def test_t(self):
        self.fail()

    def test_index(self):
        self.fail()

    def test_get_column(self):
        self.fail()

    def test_get_row(self):
        self.fail()

    def test_get_series(self):
        self.fail()

    def test_value_counts(self):
        self.fail()

    def test_series(self):
        self.fail()

    def test_get_na_n(self):
        self.fail()

    def test_map(self):
        data = [[1, 'a'], [2, 'b'], [4, 'd'], [4, 'a'], [4, 'f'], ]
        data2 = [['a', 'apple'], ['b', 'banana']]
        p2 = Pandas(data2)
        p = Pandas(data)

        output = p.map(1, p2, [0, 1])
        expect = Pandas([[1, 'apple'], [2, 'banana'], [4, ''], [4, 'apple'], [4, '']], columns=[0,1])

        self.assertEqual(output, expect)


    def test_get_list(self):
        data = [[1, 'a'], [2, 'b'], [4, 'd'], [4, 'a'], [4, 'f'], ]
        data2 = [['a', 'apple'], ['b', 'banana']]
        p2 = Pandas(data2)
        p = Pandas(data)

        output = p.get_list(add_col=False)
        expect = [[1, 'a'], [2, 'b'], [4, 'd'], [4, 'a'], [4, 'f']]

        self.assertIsInstance(output, list)
        self.assertEqual(output, expect)
