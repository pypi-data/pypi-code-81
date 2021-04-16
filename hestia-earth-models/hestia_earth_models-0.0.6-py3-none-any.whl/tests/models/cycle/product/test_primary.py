import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_product

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

    @patch(f"{class_path}._new_product", side_effect=fake_new_product)
    def test__run(self, _m):
        # only 1 product => primary
        products = [{
            '@type': 'Product',
            'term': {
                '@id': 'product-1'
            }
        }]
        self.assertEqual(_run(products)[0].get('term').get('@id'), 'product-1')

        # multiple products => primary with biggest economicValueShare
        products = [{
            '@type': 'Product',
            'term': {
                '@id': 'product-1'
            },
            'economicValueShare': 100
        }, {
            '@type': 'Product',
            'term': {
                '@id': 'product-2'
            },
            'economicValueShare': 0
        }, {
            '@type': 'Product',
            'term': {
                '@id': 'product-3'
            },
            'economicValueShare': 456464564
        }, {
            '@type': 'Product',
            'term': {
                '@id': 'product-4'
            }
        }]
        self.assertEqual(_run(products)[0].get('term').get('@id'), 'product-3')

    @patch(f"{class_path}._new_product", side_effect=fake_new_product)
    def test_run(self, _m):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
            expected = json.load(f)

        value = run(cycle)
        print(json.dumps(value, indent=2))
        self.assertEqual(value, expected)
