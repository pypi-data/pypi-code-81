# Examples of using trprimes 
from trprimes import truncp

# an iter that yields all of the left truncatable primes in 
# ascending order
ltp_iter = truncp.ordered_ltrunc()
next(ltp_iter) # yields 2
next(ltp_iter) # yields 3 and so on

# the entire list of left truncatable primes in ascending order
ltp_list = list(truncp.ordered_ltrunc())

# the number of left truncatable primes = 4260
ltp_count = truncp.count_ltrunc()

# the largest left truncatable prime = 357686312646216567629137
ltp_largest = truncp.largest_ltrunc()

