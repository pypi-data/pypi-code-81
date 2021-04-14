import random
from unittest import TestCase
from datetime import datetime

import sys
sys.path.append('./src/')

from cfjson.serde.datetime_serde import datetime_decode, datetime_encode


def test_datetimes():
	random.seed('a consistent seed')

	values = list()
	for i in range(500):
		ts = random.randrange(0, 2284101485)
		values.append(datetime.utcfromtimestamp(ts))
	return values


class Test(TestCase):

	def test_datetime_decode(self):
		for n in test_datetimes():
			blob = {
				'__json_type__': 'datetime',
				'datetime': n.isoformat()
			}
			result = datetime_decode(blob)
			self.assertEqual(result, n, msg='Failed on {}'.format(n))

	def test_datetime_encode(self):
		for n in test_datetimes():
			blob = {
				'__json_type__': 'datetime',
				'datetime': n.isoformat()
			}
			result = datetime_encode(n)
			self.assertEqual(result, blob, msg='Failed on {}'.format(n))

	def test_round_trip(self):
		for in_datetime in test_datetimes():
			out_datetime = datetime_decode(datetime_encode(in_datetime))

			self.assertEqual(in_datetime, out_datetime, msg='Failed on {}'.format(in_datetime))

	def test_datetime_decode_bad_type(self):
		blob = {
			'__json_type__': 'BadType',
			'datetime': '2021-04-07T00:00:08.114099'
		}
		self.assertRaises(TypeError, datetime_decode, blob)

	def test_datetime_decode_bad_blob(self):
		blob = {
			'datetime': '2021-04-07T00:00:08.114099'
		}
		self.assertRaises(KeyError, datetime_decode, blob)
		blob = {}
		self.assertRaises(KeyError, datetime_decode, blob)
