from decorators import exponential_backoff
from profilers import cProfile_dec

# region *start* EXPONENTIAL BACKOFF PROOF/TESTING

i = 0
dict_ = {4: 'hey'}


@exponential_backoff(rate_gain=4, max_time=4)
def myfunc(a, b, c='this'):
    global i, dict_
    print(i)
    i += 1
    print(dict_[i])
    return i

# endregion *end* EXPONENTIAL BACKOFF PROOF/TESTING


@cProfile_dec()
def prof_test():
    j = 1
    for i in range(10000000):
        j *= 1.00000001

    return j
