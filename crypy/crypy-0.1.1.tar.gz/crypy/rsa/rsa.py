import functools
import operator
import random
import math
import sympy
from crypy.utils.maths import int_root


class RSA:
    def __init__(self, n, e, d=None, factors=None):
        self.n = n
        self.e = e
        self.d = d
        self.factors = factors

        if factors is not None:
            assert n == functools.reduce(operator.mul, factors)

    @property
    def phi(self):
        return functools.reduce(operator.mul, map(lambda x: x-1, self.factors))

    @staticmethod
    def _convert(data):
        if type(data) == int:
            pass
        elif type(data) == str:
            data = int.from_bytes(data.encode(), 'big')
        elif type(data) == bytes:
            data = int.from_bytes(data, 'big')
        return data

    def encrypt(self, data):
        int_data = self._convert(data)

        return pow(int_data, self.e, self.n)

    def decrypt(self, data):
        int_data = self._convert(data)

        return pow(int_data, self.d, self.n)

    def try_find_pq(self):
        d = self.d
        e = self.e
        n = self.n

        if d is None:
            return None

        k = d*e - 1
        if k % 2 == 1:
            return None

        r = k
        t = 0
        while True:
            t += 1
            r = r//2
            if r % 2 == 1:
                break
        for i in range(100):
            g = random.randint(0, n)
            y = pow(g, r, n)
            if y != 1 and y != n-1:
                for j in range(1, t):
                    x = pow(y, 2, n)
                    if x == 1:
                        break
                    if x == n-1:
                        continue
                    y = x
                x = pow(y, 2, n)
                if x == 1:
                    break
        else:
            return None
        p = math.gcd(y - 1, n)
        q = n//p
        self.factors = [p, q]

        return p, q

    def no_modulo_attack(self, data):
        int_data = self._convert(data)
        return int_root(self.e, int_data)

    def close_primes_attack(self, quantity=2):
        middle = int_root(quantity, self.n)

        if sympy.isprime(middle):
            primes_base = [middle]
            for i in range(quantity):
                primes = primes_base[:]
                for j in range(i):  # previous
                    primes = [sympy.prevprime(primes[0])] + primes
                for j in range(quantity-i-1):  # next
                    primes = primes + [sympy.nextprime(primes[-1])]
                n = functools.reduce(operator.mul, primes)
                if n == self.n:
                    return primes
        else:
            primes_base = [sympy.prevprime(middle), sympy.nextprime(middle)]
            for i in range(1, quantity):
                primes = primes_base[:]
                for j in range(i-1):  # previous
                    primes = [sympy.prevprime(primes[0])] + primes
                for j in range(quantity-i-1):  # next
                    primes = primes + [sympy.nextprime(primes[-1])]
                n = functools.reduce(operator.mul, primes)
                if n == self.n:
                    return primes
                
        return None
