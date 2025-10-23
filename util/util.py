def degree(t: list[int]) -> int:
    """
    Get degree of the polynomial, returns -1 if t is zero polynomial
    """
    i = len(t) - 1
    while t[i] == 0:
        i -= 1

    return i if i > 0 else -1


def remove_degree(t: list[int]) -> list[int]:
    """
    Removes leading degrees and returns result e.g [1, 0, 2, 0, 0] -> [1, 0, 2]
    """
    i = len(t) - 1
    while i > 0 and t[i] == 0:
        i -= 1
    return t[:i] if i > 0 else [0]
