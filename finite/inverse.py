# module with inversion implementation for finite fields

from finite.poly_helpers import poly_egcd, poly_long_div


def inverse(f: list[int], p: int, h: list[int]) -> list[int]:
    """
    Finds inverse f^-1 of f in Z_p[X]/(h) using Extended Euclidean Algorithm
    Returns None if f is zero or if inverse doesn't exist
    """
    # Check if f is zero polynomial (no inverse)
    if not f or (len(f) == 1 and f[0] == 0):
        return None

    # Use extended Euclidean algorithm: a*f + b*h = gcd(f, h)
    # If h is irreducible and f != 0, then gcd(f, h) = 1
    # So a*f + b*h = 1, which means a*f ≡ 1 (mod h)
    # Therefore a is the inverse of f in Zp[X]/(h)
    a, b, d = poly_egcd(f, h, p)

    # Check if gcd is not 1 (inverse doesn't exist)
    if d is None or not (len(d) == 1 and d[0] == 1):
        return None

    # a is the inverse, but we need to ensure it's in canonical form (mod h)
    _, a_reduced = poly_long_div(a, h, p)

    if a_reduced is None:
        return [0]

    return a_reduced
