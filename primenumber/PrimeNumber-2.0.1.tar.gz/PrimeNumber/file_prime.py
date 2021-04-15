from math import sqrt


def pre_check(n: int):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Please enter an integer.")
    if n <= 0:
        raise ValueError("Please enter an integer greater than zero")


class Prime:
    def __init__(self):
        self.list_prime_numbers = []

    def is_prime(self, n: int):
        pre_check(n)
        if n == 1:
            return False  # We are considering that a prime number has to have exactly two distinct factors
        gen = self.generator()
        while True:
            div_prime = next(gen)
            if n % div_prime == 0:
                return False
            if div_prime > sqrt(n):
                return True

    def generator(self):
        def aux_infinite_seq():
            num = 3
            while True:
                yield num
                num += 1

        prime = 2
        self.list_prime_numbers.append(prime)
        aux_gen = aux_infinite_seq()
        while True:
            next_ = next(aux_gen)
            control = True
            for i in self.list_prime_numbers:
                if i > sqrt(next_):
                    pass
                else:
                    if next_ % i == 0:
                        control = False
                        break
            if control:
                yield prime
                prime = next_
                self.list_prime_numbers.append(prime)

    def prime_factors(self, n: int):
        pre_check(n)
        control = self.is_prime(n)
        if control or n == 1:
            return [n]
        else:
            prime_factors_list = []
            gen_2 = self.generator()
            while True:
                factor = next(gen_2)
                if n % factor == 0:
                    n = int(n / factor)
                    prime_factors_list.append(factor)
                    if self.is_prime(n):
                        prime_factors_list.append(n)
                        break
                    gen_2 = self.generator()
                    if n == 1:
                        break
        return sorted(prime_factors_list)
