def batch(I, batch_size=1000):
    """
    Takes an iterator `I` and produces an iterator
    which yields elements from `I` grouped in batches
    of size `batch_size` (default is 1000).
    """
    k = 0
    l = list()
    for i in I:
        k += 1
        l.append(i)
        if k >= batch_size:
            yield l
            k = 0
            l = []
    if l:
        yield l

def batch2(I, batch_size):
    try:
        while True:
            l = list()
            for k in range(batch_size):
                l.append(next(I))
            yield l
    except StopIteration:
        if l:
            yield l
