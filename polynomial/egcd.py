# module with extended euclidean algorithm implementation

from polynomial import mult_div
from polynomial import add_sub


def egcd(a: list[int], b: list[int], p: int) -> tuple[list[int], list[int], list[int]]:
    """
    Finds x, y, d such that:
    x * a + y * b = d, in Z_p[X],
    where d = gcd(a, b)

    and returns x, y, d (in this order)
    """

    while a and a[-1] == 0:
        a.pop()
    while b and b[-1] == 0:
        b.pop()

    x, v = [1], [1]
    y, u = [0], [0]

    while b and any(c != 0 for c in b):
        q, r = mult_div.div(a, b, p)
        a, b = b, r
        xt, yt = x, y
        x, y = u, v
        u = add_sub.sub(xt, mult_div.mult(q, u, p), p)
        v = add_sub.sub(yt, mult_div.mult(q, v, p), p)

    while a and a[-1] == 0:
        a.pop()

    # monic gcd
    if a:
        lc_a_inv = pow(a[-1], p - 2, p)
        a = mult_div.mult(a, [lc_a_inv], p)
        x = mult_div.mult(x, [lc_a_inv], p)
        x = x if x else [0]
        y = mult_div.mult(y, [lc_a_inv], p)
        y = y if y else [0]

    return x, y, a
