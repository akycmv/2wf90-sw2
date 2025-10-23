# module with multiplication, division of polynomials in finite fields

from finite.poly_helpers import poly_mult, poly_long_div


def mult(f: list[int], g: list[int], p: int, h: list[int]) -> list[int]:
    """
    Returns f * g in Z_p[X]/(h) in canonical form
    """
    # Multiply polynomials in Zp[X]
    product = poly_mult(f, g, p)

    # Reduce modulo h to get canonical form
    _, remainder = poly_long_div(product, h, p)

    # Handle None case (shouldn't happen with valid h)
    if remainder is None:
        return [0]

    return remainder


def div(f: list[int], g: list[int], p: int, h: list[int]) -> list[int]:
    """
    Divides f by g in Z_p[X]/(h) and returns f/g = f * g^(-1) in canonical form
    Returns None if g is zero (division undefined)
    """
    from finite.inverse import inverse

    # Check if g is zero polynomial (division undefined)
    if not g or (len(g) == 1 and g[0] == 0):
        return None

    # Compute g^(-1) in the finite field
    g_inv = inverse(g, p, h)

    # If inverse doesn't exist (shouldn't happen if h is irreducible), return None
    if g_inv is None:
        return None

    # Compute f * g^(-1) mod h
    return mult(f, g_inv, p, h)
