from flask_scenario_testing.backend.modifiers.Modifier import Modifier
import time


def fib(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class Fibonacci(Modifier):
    def identifier(self):
        return 'FIB'

    def modify(self, fun, endpoint_name, modifier_args: dict):
        def wrapper(*args, **kwargs):
            N = modifier_args['N']

            start = time.time()
            fib_result = fib(N)
            ms = (time.time() - start) * 1000

            print("FIB({}) = {} ({}ms)".format(N, fib_result, ms))

            return fun(*args, **kwargs)

        return wrapper
