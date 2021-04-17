def int_root (n, radicand):
    if radicand < 2:
        return radicand
    a1 = n - 1
    c = 1
    d = (a1 * c + radicand // (c ** a1)) // n
    e = (a1 * d + radicand // (d ** a1)) // n
    while c not in (d, e):
        c, d, e = d, e, (a1 * e + radicand // (e ** a1)) // n
    return min(d, e)
