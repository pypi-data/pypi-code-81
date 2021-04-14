import unittest
import sympy

from truncp import largest_ltrunc, count_ltrunc, ordered_ltrunc

class TestTruncPrimes(unittest.TestCase):

	# the largest left truncatable prime, verified from external sources
	def test_largest_ltrunc(self):
		result = largest_ltrunc()
		self.assertEqual(result, 357686312646216567629137)

	# the number ofleft truncatable primes, verified from external sources
	def test_count_ltrunc(self):
		result = count_ltrunc()
		self.assertEqual(result, 4260)

	def test_ordered_ltrunc(self):
		# get the list of ordered left truncatable primes
		ordered_list = [p for p in ordered_ltrunc()]

		# the length of the list should be equal to count_ltrunc()
		n1 = count_ltrunc()
		n2 = len(ordered_list)
		self.assertEqual(n1, n2)
		
		# all the numbers in the list should at least be prime
		for p in ordered_list:
			result = sympy.isprime(p)
			self.assertTrue(result)
		
		# they should be in ascending order
		sorted_list = sorted(ordered_list)
		self.assertEqual(ordered_list,sorted_list)

