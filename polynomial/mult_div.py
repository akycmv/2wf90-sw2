# module with implementations of multiplication and (long) division

from util.util import degree, remove_degree


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
    return remove_degree(out)


def div(f: list[int], g: list[int], p: int) -> tuple[list[int], list[int]]:
    """
    Divides f by g in Z_p[X] using long division and returns q, r (in this order) such that
    f = q * g + r
    """

    f = remove_degree(f[:])
    g = remove_degree(g[:])

    deg_f = degree(f)
    deg_g = degree(g)

    if deg_f < deg_g or deg_f < 0:
        return [0], f

    q = []
    r = f[:]

    lc_g = g[deg_g]
    lc_g_inv = pow(lc_g, p - 2, p)

    deg_r = degree(r)

    while deg_r >= deg_g and deg_r >= 0:
        lc_r = r[deg_r]
        coeff = (lc_r * lc_g_inv) % p
        shift = deg_r - deg_g

        while len(q) <= shift:
            q.append(0)
        q[shift] = (q[shift] + coeff) % p

        for i in range(len(g)):
            if i + shift < len(r):
                r[i + shift] = (r[i + shift] - coeff * g[i]) % p

        deg_r = degree(r)

    q = remove_degree(q if q else [0])
    r = remove_degree(r)

    return q, r
