# module with primitivity (check, generation) for finite fields

from finite.poly_helpers import poly_pow, get_prime_factors
from random import randint


def check(f: list[int], p: int, h: list[int]) -> bool:
    """
    Checks if f is primitive for Z_p[X]/(h)

    A primitive element generates the multiplicative group of order q-1,
    where q = p^deg(h) is the size of the finite field.

    Algorithm:
    1. Check f^(q-1) ≡ 1 (mod h)
    2. For all prime divisors p_i of (q-1), check f^((q-1)/p_i) ≢ 1 (mod h)
    """
    # Handle zero polynomial (not primitive)
    if not f or (len(f) == 1 and f[0] == 0):
        return False

    # Compute field size q = p^deg(h)
    n = len(h) - 1  # deg(h)
    q = p ** n
    order = q - 1  # Order of multiplicative group

    # Check if f^(q-1) ≡ 1 (mod h)
    f_pow_order = poly_pow(f, order, h, p)
    if not (len(f_pow_order) == 1 and f_pow_order[0] == 1):
        return False

    # Get prime factors of (q-1)
    prime_factors = get_prime_factors(order)

    # For each prime factor p_i, check that f^((q-1)/p_i) ≢ 1 (mod h)
    for prime in prime_factors:
        exponent = order // prime
        f_pow = poly_pow(f, exponent, h, p)
        # If f^((q-1)/p_i) ≡ 1, then f is not primitive
        if len(f_pow) == 1 and f_pow[0] == 1:
            return False

    return True


def generate(p: int, h: list[int]) -> list[int]:
    """
    Generates a primitive element f in Z_p[X]/(h)

    Algorithm: Generate random elements and test for primitivity
    """
    n = len(h) - 1  # deg(h)

    # Try random polynomials of degree < n
    max_attempts = 10000  # Safety limit
    attempts = 0

    while attempts < max_attempts:
        # Generate random polynomial of degree < n with coefficients in [0, p-1]
        f = [randint(0, p - 1) for _ in range(n)]

        # Normalize: remove leading zeros, but ensure non-zero polynomial
        while len(f) > 1 and f[-1] == 0:
            f.pop()

        # Skip zero polynomial
        if len(f) == 1 and f[0] == 0:
            attempts += 1
            continue

        # Check if primitive
        if check(f, p, h):
            return f

        attempts += 1

    # Fallback: try simple elements like [1, 0], [0, 1], etc.
    for i in range(n):
        f = [0] * n
        f[i] = 1
        if check(f, p, h):
            return f

    # Should never reach here for valid irreducible h
    return [1]  # Return [1] as last resort
