# module with implementations of multiplication and (long) division

from util.util import remove_degree


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


def div(
    f: list[int], g: list[int], p: int
) -> tuple[list[int], list[int]] | tuple[None, None]:
    """
    Divides f by g in Z_p[X] using long division and returns q, r (in this order) such that
    f = q * g + r

    Returns None if division by zero polynomial.
    """

    f = remove_degree(f[:])
    g = remove_degree(g[:])

    if not g or all(c == 0 for c in g):
        return None, None

    if not f or all(c == 0 for c in f):
        return [0], [0]

    if len(f) < len(g):
        return [0], f

    q = [0] * (len(f) - len(g) + 1)
    r = f[:]

    lead_g = g[-1] % p
    inv_lead_g = __mod_inverse(lead_g, p)

    for i in range(len(f) - len(g), -1, -1):
        r = remove_degree(r)

        if len(r) >= len(g) + i:
            coeff = (r[-1] * inv_lead_g) % p
            q[i] = coeff

            for j in range(len(g)):
                r[i + j] = (r[i + j] - coeff * g[j]) % p

    q = remove_degree(q) if q else [0]
    r = remove_degree(r) if r else [0]

    return q, r


def __mod_inverse(a: int, p: int) -> int:
    """
    Find modular inverse of a modulo p using Fermat's Little Theorem
    """
    return pow(a, p - 2, p)
