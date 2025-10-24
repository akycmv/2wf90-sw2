# module with helper functions for finite field operations
# Uses existing polynomial arithmetic from polynomial module

from polynomial.mult_div import mult as poly_mult, div as poly_div


def get_prime_factors(n: int) -> list[int]:
    """
    Returns list of unique prime factors of n using trial division

    Used for primitivity checking: we need to verify that an element's
    order is exactly (q-1), which requires checking divisibility by
    prime factors of (q-1).
    """
    factors = set()
    d = 2
    # Trial division: test divisors up to sqrt(n)
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            # Remove all factors of d from n
            while n % d == 0:
                n //= d
        d += 1
    # If n > 1 after trial division, n itself is prime
    if n > 1:
        factors.add(n)
    return list(factors)


def poly_pow(base: list[int], exp: int, mod: list[int], p: int) -> list[int]:
    """
    Computes base^exp mod (mod) in Z_p[X] using binary exponentiation

    This is used for primitivity checking where we need to compute
    large powers like f^(q-1) efficiently. Binary exponentiation
    reduces O(exp) multiplications to O(log exp).
    """
    res = [1]  # Start with identity element 1

    # Reduce base modulo mod to ensure we work with canonical representatives
    _, base_rem = poly_div(base, mod, p)
    if base_rem is None or not base_rem:
        base_rem = base

    # Binary exponentiation: process exp bit by bit
    while exp > 0:
        # If current bit is 1, multiply result by current base power
        if exp % 2 == 1:
            res = poly_mult(res, base_rem, p)
            # Ensure zero polynomial is represented as [0]
            if not res:
                res = [0]
            # Reduce modulo mod to maintain canonical form
            _, res = poly_div(res, mod, p)
            if not res:
                res = [0]

        # Square the base for next bit position
        base_rem = poly_mult(base_rem, base_rem, p)
        if not base_rem:
            base_rem = [0]
        # Reduce modulo mod to maintain canonical form
        _, base_rem = poly_div(base_rem, mod, p)
        if not base_rem:
            base_rem = [0]

        # Move to next bit
        exp //= 2

    return res if res else [0]
