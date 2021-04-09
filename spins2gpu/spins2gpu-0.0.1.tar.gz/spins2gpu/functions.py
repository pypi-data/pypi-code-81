from numba import vectorize

@vectorize(['int8(float32)'], target='cuda')
def int(randval):
    return 1 if randval > 0.5 else -1
