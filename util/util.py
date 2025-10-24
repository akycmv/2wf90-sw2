def remove_degree(t: list[int]) -> list[int]:
    """
    Removes leading degrees and returns result e.g [1, 0, 2, 0, 0] -> [1, 0, 2]
    """
    i = len(t) - 1
    while i > 0 and t[i] == 0:
        i -= 1
    return t[: i + 1]
