# module with implementations of addition and subtraction

from util.util import remove_degree


def add(f: list[int], g: list[int], p: int) -> list[int]:
    """
    Adds polynomials f, g in Z_p[X] and returs f + g
    """

    if len(f) < len(g):
        f, g = g, f

    n = len(f)
    # pad smaller one with zeroes
    g = g + [0] * (n - len(g))
    # in polynomials resulting degree is at most that of the larger one
    out = [0 for _ in range(n)]
    for i in range(n):
        out[i] = f[i] + g[i]
        out[i] = out[i] % p

    # remove trailing degrees e.g [0, 1, 2, 3, 0] -> [0, 1, 2, 3]
    return remove_degree(out)


def sub(f: list[int], g: list[int], p: int) -> list[int]:
    """
    Subtracts g from f in Z_p[X] and returns result
    """

    n = 0
    if len(f) < len(g):
        n = len(g)
        f = f + [0] * (n - len(f))
    else:
        n = len(f)
        g = g + [0] * (n - len(g))

    out = [0 for _ in range(n)]
    for i in range(n):
        out[i] = f[i] - g[i]
        out[i] = out[i] % p

    return remove_degree(out)
