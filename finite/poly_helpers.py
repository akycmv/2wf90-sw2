# module with helper functions for finite field operations
# Uses existing polynomial arithmetic from polynomial module

from polynomial.mult_div import mult as poly_mult, div as poly_div


def get_prime_factors(n):
    """
    Returns list of unique prime factors of n
    """
    factors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return list(factors)


def poly_pow(base, exp, mod, p):
    """
    Computes base^exp mod (mod) in Z_p[X] using binary exponentiation
    """
    res = [1]
    _, base_rem = poly_div(base, mod, p)
    if base_rem is None or not base_rem:
        base_rem = base

    while exp > 0:
        if exp % 2 == 1:
            res = poly_mult(res, base_rem, p)
            if not res:
                res = [0]
            _, res = poly_div(res, mod, p)
            if not res:
                res = [0]
        base_rem = poly_mult(base_rem, base_rem, p)
        if not base_rem:
            base_rem = [0]
        _, base_rem = poly_div(base_rem, mod, p)
        if not base_rem:
            base_rem = [0]
        exp //= 2

    return res if res else [0]
