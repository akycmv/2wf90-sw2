# module with implementations of multiplication and (long) division


def mult(f: list[int], g: list[int], p: int) -> list[int]:
    """
    Multiplies f by g and returns result in Z_p[X]
    """

    if not f or not g:
        return []
    elif (len(f) == 1 and f[0] == 0) or (len(g) == 1 and g[0] == 0):
        return []

    # resulting degree is at most len(f) + len(g)
    out = [0 for _ in range(len(f) + len(g))]

    for i in range(len(f)):
        for j in range(len(g)):
            out[i + j] = (out[i + j] + f[i] * g[j]) % p

    # remove trailing degrees
    i = len(out)
    while i > 0 and out[i - 1] == 0:
        i -= 1

    return out[:i]


def div(f: list[int], g: list[int], p: int) -> tuple[list[int], list[int]]:
    """'
    Divides f by g in Z_p[X] using long division and returns q, r (in this order) such that
    f = q * g + r
    """

    # f = 0 * g + f
    if len(f) < len(g):
        return [0], f

    while f and f[-1] == 0:
        f.pop()

    while g and g[-1] == 0:
        g.pop()

    # algorithm taken from Algebra for Security script, page 21, algorithm 2.2.2 (Long Division)

    q = [0 for _ in range(len(f))]
    r = f.copy()

    deg_r = len(r) - 1
    deg_g = len(g) - 1

    # lc(g), lc(g)^-1
    lc_g = g[deg_g]
    lc_g_inv = pow(lc_g, p - 2, p)

    # while deg(r) >= deg(g)
    while deg_r >= deg_g and deg_r >= 0:
        lc_r = r[deg_r]

        # lc(r) * lc(g)^-1
        coef = (lc_r * lc_g_inv) % p
        dd = deg_r - deg_g

        # q = q + coef * ...
        q[dd] = (q[dd] + coef) % p

        # r = r - coef * ...
        for i in range(deg_g + 1):
            r[i + dd] = (r[i + dd] - coef * g[i]) % p

        # shift degree
        while deg_r >= 0 and r[deg_r] == 0:
            deg_r -= 1

    # remove leading degrees
    qi, ri = len(q), len(r)

    while qi > 0 and q[qi - 1] == 0:
        qi -= 1

    while ri > 0 and r[ri - 1] == 0:
        ri -= 1

    return q[:qi] if qi != 0 else [0], r[:ri] if ri != 0 else [0]
