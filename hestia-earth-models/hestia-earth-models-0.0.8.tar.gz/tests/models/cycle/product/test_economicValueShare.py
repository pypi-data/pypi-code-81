import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_product

from hestia_earth.models.cycle.product.economicValueShare import run, _should_run, _should_run_p

class_path = 'hestia_earth.models.cycle.product.economicValueShare'
fixtures_folder = f"{fixtures_path}/cycle/product/economicValueShare"


class TestProductEconomicValueShare(unittest.TestCase):
    def test_should_run(self):
        # if total value >= 100, do nothing
        products = [{
            '@type': 'Product',
            'economicValueShare': 20
        }, {
            '@type': 'Product',
            'economicValueShare': 80
        }, {
            '@type': 'Product'
        }]
        self.assertEqual(_should_run(products), False)

        # total < 100 => run
        products[1]['economicValueShare'] = 70
        self.assertEqual(_should_run(products), True)

    def test_should_run_product(self):
        product = {'@type': 'Product'}
        self.assertEqual(_should_run_p(product), True)

        product['economicValueShare'] = 20
        self.assertEqual(_should_run_p(product), False)

    @patch(f"{class_path}._new_product", side_effect=fake_new_product)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
