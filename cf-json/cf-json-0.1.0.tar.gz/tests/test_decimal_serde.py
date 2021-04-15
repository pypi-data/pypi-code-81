import itertools
from unittest import TestCase
from decimal import Decimal

from cfjson.serde.decimal_serde import decimal_decode, decimal_encode

import sys
sys.path.append('./src/')


def test_numbers_extreme():
	permutations = set()
	for sign_char in ('-', '', ' ', '+'):
		for perm in itertools.permutations(('1', '1', '', '.', '0', '9')):
			permutations.add(sign_char + ''.join(perm))
	return list(permutations)


class Test(TestCase):

	def test_decimal_decode(self):
		for n in test_numbers_extreme():
			blob = {
				'__json_type__': 'Decimal',
				'decimal': n
			}
			result = decimal_decode(blob)
			self.assertEqual(result, Decimal(n), msg='Failed on {}'.format(n))

	def test_decimal_encode(self):
		for n in test_numbers_extreme():
			blob = {
				'__json_type__': 'Decimal',
				'decimal': str(Decimal(n))
			}
			result = decimal_encode(Decimal(n))
			self.assertEqual(result, blob, msg='Failed on {}'.format(n))

	def test_round_trip(self):
		for n in test_numbers_extreme():
			in_number = Decimal(n)
			out_number = decimal_decode(decimal_encode(in_number))

			self.assertEqual(in_number, out_number, msg='Failed on {}'.format(n))

	def test_decimal_decode_bad_type(self):
		blob = {
			'__json_type__': 'BadType',
			'decimal': '1.0'
		}
		self.assertRaises(TypeError, decimal_decode, blob)

	def test_decimal_decode_bad_blob(self):
		blob = {
			'decimal': '1.0'
		}
		self.assertRaises(KeyError, decimal_decode, blob)
		blob = {}
		self.assertRaises(KeyError, decimal_decode, blob)
