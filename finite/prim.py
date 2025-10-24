# module with primitivity (check, generation) for finite fields

from finite.poly_helpers import poly_pow, get_prime_factors
from random import randint


def check(f: list[int], p: int, h: list[int]) -> bool:
    """
    Checks if f is primitive for Z_p[X]/(h)

    A primitive element generates the multiplicative group of order q-1,
    where q = p^deg(h) is the size of the finite field.

    Algorithm (based on lecture notes):
    1. Check f^(q-1) ≡ 1 (mod h) - f must be in multiplicative group
    2. For all prime divisors p_i of (q-1), check f^((q-1)/p_i) ≢ 1 (mod h)
       This ensures f has full order (q-1), not a proper divisor
    """
    # Handle zero polynomial (not primitive - not in multiplicative group)
    if not f or (len(f) == 1 and f[0] == 0):
        return False

    # Compute field size q = p^deg(h) and multiplicative group order
    n = len(h) - 1  # deg(h): degree of irreducible polynomial
    q = p ** n      # |F_q| = p^n: size of finite field
    order = q - 1   # |F_q*| = q-1: size of multiplicative group

    # First check: f must be in the multiplicative group (f^(q-1) = 1)
    f_pow_order = poly_pow(f, order, h, p)
    if not (len(f_pow_order) == 1 and f_pow_order[0] == 1):
        return False

    # Get prime factors of (q-1) for full order verification
    prime_factors = get_prime_factors(order)

    # Second check: f must have FULL order (q-1), not a proper divisor
    # If f^((q-1)/p_i) = 1 for some prime p_i, then order divides (q-1)/p_i
    for prime in prime_factors:
        exponent = order // prime
        f_pow = poly_pow(f, exponent, h, p)
        # If f^((q-1)/p_i) ≡ 1, then f has order < (q-1), not primitive
        if len(f_pow) == 1 and f_pow[0] == 1:
            return False

    return True


def generate(p: int, h: list[int]) -> list[int]:
    """
    Generates a primitive element f in Z_p[X]/(h)

    Algorithm: Probabilistic search with random sampling
    Primitive elements are plentiful in finite fields, so random
    testing typically succeeds quickly.
    """
    n = len(h) - 1  # deg(h): degree of irreducible polynomial

    # Main strategy: random sampling
    max_attempts = 10000  # Safety limit to prevent infinite loops
    attempts = 0

    while attempts < max_attempts:
        # Generate random polynomial of degree < n with coefficients in [0, p-1]
        # Each polynomial represents an element of F_q where q = p^n
        f = [randint(0, p - 1) for _ in range(n)]

        # Normalize: remove leading zeros to maintain canonical form
        while len(f) > 1 and f[-1] == 0:
            f.pop()

        # Skip zero polynomial (not in multiplicative group)
        if len(f) == 1 and f[0] == 0:
            attempts += 1
            continue

        # Test if this random element is primitive
        if check(f, p, h):
            return f

        attempts += 1

    # Fallback strategy: systematically try simple monomial elements
    # Try X^i for i = 0, 1, ..., n-1 (represented as [0,...,0,1,0,...,0])
    for i in range(n):
        f = [0] * n
        f[i] = 1  # Set coefficient of X^i to 1
        if check(f, p, h):
            return f

    # Last resort: return constant 1 (usually not primitive, but valid element)
    # Should never reach here for valid irreducible h
    return [1]
