# module for polynomial addition, subtraction implementation for finite fields


def add(f: list[int], g: list[int], p: int, h: list[int]) -> list[int]:
    """
    Adds f, g in Z_p[X]/(h) and returns result
    """

    # TODO: same trick as before
    # (-x) + y = y - x
    # x + (-y) = x - y
    # (-x) + (-y) = - (x + y)
    return []


def sub(f: list[int], g: list[int], p: int, h: list[int]) -> list[int]:
    """
    Subtracts g from f in Z_p[X]/(h) and returns result
    """

    # TODO: same trick as before
    # x - (-y) = x+y
    # (-x) - y = - (x+y)
    # -x - (-y) = y - x
    # in case deg(g) > deg(f) we switch places, as f - g = - (g - f)
    return []
