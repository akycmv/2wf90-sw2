# module with irreducibility (check, generation) implementations

from polynomial import egcd
from polynomial import add_sub
import random


def check(f: list[int], p: int) -> bool:
    """
    Checks if f is irreducible in Z_mod[X]
    """

    # algorithm taken from Algebra for Security script, page 72, algorithm 7.1.4 (Testing irreducibility)
    # TODO: testing irreducibility 2, 7.1.6

    t = 1

    while True:
        # g = X^(q^t) - X
        # X^(q^t) = [0 ... 1], len = q^t
        # X = [0, 1]
        g = [0 for _ in range(pow(p, t))]
        g[-1] = 1
        g = add_sub.sub(g, [0, 1], p)

        _, _, gcd = egcd.egcd(f, g, p)
        if gcd != [1]:
            break

        t += 1

    return t == len(f) - 1


def generate(n: int, p: int) -> list[int]:
    """
    Generates irreducible element of degree n in Z_p[X]
    """

    # algorithm taken from Algebra for Security script, page 73, algorithm 7.1.7 (Generating an Irreducible Polynomial II)

    # f = rand poly of deg n; while f reducible generate new f
    f = __rand_poly(n, p)
    while not check(f, p):
        f = __rand_poly(n, p)
    return f


def __rand_poly(n: int, p: int) -> list[int]:
    """
    Generates random polynomial of degree n in Z_p[X]
    """

    # random polynomial of degree n, degree n => lc != 0
    f = random.sample(range(0, p), n)
    while f[-1] == 0:
        f[-1] = random.randint(1, p)

    return f
