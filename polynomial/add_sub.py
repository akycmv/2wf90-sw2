# module with implementations of addition and subtraction


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
    i = n
    while i > 0 and out[i - 1] == 0:
        i -= 1
    return out[:i]


def sub(f: list[int], g: list[int], p: int) -> list[int]:
    """
    Subtracts g from f in Z_p[X] and returns result
    """

    if len(f) < len(g):
        f, g = g, f

    n = len(f)
    g = g + [0] * (n - len(g))

    out = [0 for _ in range(n)]
    for i in range(n):
        out[i] = f[i] - g[i]
        out[i] = out[i] % p

    i = n
    while i > 0 and out[i - 1] == 0:
        i -= 1

    return out[:i]
