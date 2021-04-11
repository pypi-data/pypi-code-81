def pick(arr, key):
    return [getattr(x, key) for x in arr]

