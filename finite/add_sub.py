# module for polynomial addition, subtraction implementation for finite fields

from polynomial.add_sub import add as poly_add, sub as poly_sub


def add(f: list[int], g: list[int], p: int, h: list[int]) -> list[int]:
    """
    Adds f, g in Z_p[X]/(h) and returns result in canonical form
    """
    # In finite field Zp[X]/(h), addition is just polynomial addition mod p
    # Since inputs are in canonical form (deg < deg(h)), result is also < deg(h)
    result = poly_add(f, g, p)

    # Ensure result is not empty (return [0] for zero polynomial)
    if not result or len(result) == 0:
        return [0]

    return result


def sub(f: list[int], g: list[int], p: int, h: list[int]) -> list[int]:
    """
    Subtracts g from f in Z_p[X]/(h) and returns result in canonical form
    """
    # In finite field Zp[X]/(h), subtraction is just polynomial subtraction mod p
    # Since inputs are in canonical form (deg < deg(h)), result is also < deg(h)
    result = poly_sub(f, g, p)

    # Ensure result is not empty (return [0] for zero polynomial)
    if not result or len(result) == 0:
        return [0]

    return result
