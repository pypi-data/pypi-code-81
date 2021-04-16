import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_product

from hestia_earth.models.cycle.product.revenue import run, _should_run

class_path = 'hestia_earth.models.cycle.product.revenue'
fixtures_folder = f"{fixtures_path}/cycle/product/revenue"


class TestProductRevenue(unittest.TestCase):
    def test_should_run(self):
        product = {'@type': 'Product'}
        self.assertEqual(_should_run(product), False)

        product['value'] = [1]
        self.assertEqual(_should_run(product), False)

        product['price'] = 1
        self.assertEqual(_should_run(product), True)

        product['revenue'] = 2
        self.assertEqual(_should_run(product), False)

    @patch(f"{class_path}._new_product", side_effect=fake_new_product)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
