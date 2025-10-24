# module with extended euclidean algorithm implementation

from polynomial import mult_div
from polynomial import add_sub
from util.util import remove_degree


def egcd(
    a: list[int], b: list[int], p: int
) -> tuple[list[int], list[int], list[int]] | tuple[None, None, None]:
    """
    Finds x, y, d such that:
    x * a + y * b = d, in Z_p[X],
    where d = gcd(a, b)

    and returns x, y, d (in this order)
    """

    # algorithm taken from Algebra for Security script, page 27, algorithm 2.3.10 (Extended Euclidean algorithm for polynomials)

    a = remove_degree(a)
    b = remove_degree(b)

    x, v = [1], [1]
    y, u = [0], [0]

    while b and any(c != 0 for c in b):
        q, r = mult_div.div(a, b, p)
        if not q or not r:
            return None, None, None
        a, b = b, r
        xt, yt = x, y
        x, y = u, v
        u = add_sub.sub(xt, mult_div.mult(q, u, p), p)
        v = add_sub.sub(yt, mult_div.mult(q, v, p), p)

    a = remove_degree(a)
    x = remove_degree(x)
    y = remove_degree(y)

    # monic gcd
    if a:
        lc_a_inv = pow(a[-1], p - 2, p)
        a = mult_div.mult(a, [lc_a_inv], p)
        x = mult_div.mult(x, [lc_a_inv], p)
        x = x if x else [0]
        y = mult_div.mult(y, [lc_a_inv], p)
        y = y if y else [0]

    return x, y, a
