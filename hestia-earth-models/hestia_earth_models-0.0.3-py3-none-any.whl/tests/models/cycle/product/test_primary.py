import unittest
import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.product.primary import run, _should_run, _run

class_path = 'hestia_earth.models.cycle.product.primary'
fixtures_folder = f"{fixtures_path}/cycle/product/primary"


class TestProductPrimary(unittest.TestCase):
    def test_should_run(self):
        # no products => do not gap-fill
        products = []
        self.assertEqual(_should_run(products), False)

        # with product but no primary info => gap-fill
        product = {
            '@type': 'Product'
        }
        products.append(product)
        self.assertEqual(_should_run(products), True)

        # with product with primary => no gap-fill
        product['primary'] = True
        self.assertEqual(_should_run(products), False)

    def test__run(self):
        # only 1 product => primary
        products = [{
            '@type': 'Product'
        }]
        self.assertEqual(_run(products)[0]['primary'], True)

        # multiple products => primary with biggest economicValueShare
        products = [{
            '@type': 'Product',
            'economicValueShare': 100
        }, {
            '@type': 'Product',
            'economicValueShare': 0
        }, {
            '@type': 'Product',
            'economicValueShare': 456464564
        }, {
            '@type': 'Product'
        }]
        self.assertEqual(_run(products)[2]['primary'], True)

    def test_run(self):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        self.assertEqual(value, expected)
