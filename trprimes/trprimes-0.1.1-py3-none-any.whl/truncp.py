"""
Programming problems related to prime numbers.  A good source of fodder
for number theory and prime number problems is the youtube channel 
https://www.youtube.com/user/numberphile
"""
from collections import namedtuple
from sympy import isprime

# this produces the left truncatable prime with the larges value
# there must be more graceful ways to do it
def largest_ltrunc():
	"""
	Computes the largest left truncatable prime https://youtu.be/azL5ehbw_24
	A left truncatable prime is still prime when the left most digit is
	dropped.  For example 317 -> 17 -> 7 are prime so 317 is a left 
	truncatable prime

	returns 357686312646216567629137
	"""

	# Prime.value is the value of the prime number
	# Prime.k is the power of 10 needed to generate the first digit
	Prime = namedtuple('Prime',['value','k'])

	# list single digit prime numbers
	prime_list = [Prime(x,0) for x in (2,3,5,7)]

	# the largest single digit prime number
	N = max([prime.value for prime in prime_list])

	# pop from the front of the list then
	# keep adding left truncatable primes derived from it
	while prime_list:
		prime = prime_list.pop(0)

		# digits 1,...,9 are valid left additions 
		for t in range(1,10):
			n = t*10**(prime.k + 1) + prime.value

			# if the number is prime it is a left truncatable prime
			# add it to the list and see if it is the largest
			if isprime(n):
				prime_list.append(Prime(n,prime.k + 1))
				N = max(n,N)

	return N

# this counts the number of left truncatable primes
def count_ltrunc():
	"""
	Counts the number of left truncatable primes https://youtu.be/azL5ehbw_24
	A left truncatable prime is still prime when the left most digit is
	dropped.  For example 317 -> 17 -> 7 are prime so 317 is a left 
	truncatable prime

	returns 4260
	"""
	

	# Prime.value is the value of the prime number
	# Prime.k is the power of 10 needed to generate the first digit
	Prime = namedtuple('Prime',['value','k'])

	# list single digit prime numbers
	prime_list = [Prime(x,0) for x in (2,3,5,7)]

	count = 0

	# pop from the front of the list then
	# keep adding left truncatable primes derived from it
	while prime_list:
		prime = prime_list.pop(0)
		count += 1

		# digits 1,...,9 are valid left additions 
		for t in range(1,10):
			n = t*10**(prime.k + 1) + prime.value

			# if the number is prime it is a left truncatable prime
			# add it to the list and see if it is the largest
			if isprime(n):
				prime_list.append(Prime(n,prime.k + 1))

	return count


# an iterator that produces left truncatable primes in increasing order
# while storing a minimal number of unused values
def ordered_ltrunc():
	"""
	Iterates through the left truncatable prime https://youtu.be/azL5ehbw_24
	A left truncatable prime is still prime when the left most digit is
	dropped.  For example 317 -> 17 -> 7 are prime so 317 is a left 
	truncatable prime

	returns an iterator that goes through them in increasing order
	"""

	# Prime.value is the value of the prime number
	# Prime.k is the power of 10 needed to generate the first digit
	Prime = namedtuple('Prime',['value','k'])

	# list single digit prime numbers
	working_list = [Prime(x,0) for x in (2,3,5,7)]

	# stores the set of left truncatable primes that have one more
	# digit than the working list
	expanding_list = []

	# the expanding is built with the primes ordered
	while working_list:
		# digits 1,...,9 are valid left additions 
		for t in range(1,10):
			for prime in working_list:
				n = t*10**(prime.k + 1) + prime.value
				# the left additions just got constructed in ascending order
				# if the number is prime it is a left truncatable prime
				# add it to the expanding list
				if isprime(n):
					expanding_list.append(Prime(n,prime.k + 1))

		# the expanding list is built so yield the working list one by one
		while working_list:
			yield working_list.pop(0).value

		# working list is exhausted - replace it with the expanding list
		working_list = expanding_list

		# start a new expanding list
		expanding_list = []
