# module with irreducibility (check, generation) implementations

from polynomial import egcd
import random
from util.util import remove_degree


def check(f: list[int], p: int) -> bool:
    """
    Checks if f is irreducible in Z_p[X]
    """

    f = remove_degree(f)
    n = len(f) - 1
    if n < 2:
        return True

    # algorithm taken from Algebra for Security script, page 72, algorithm 7.1.6 (Testing irreducibility II)

    i = 0
    pdivs = __prime_divisors(n)
    k = len(pdivs)

    # check gcd(f, X^(p^t) - X) = 1 for all t = n/p_i
    while i < k:
        t = n // pdivs[i]

        # g = X^(p^t) - X
        g = __pow_poly(p, t)

        _, _, gcd = egcd.egcd(f, g, p)
        gcd = remove_degree(gcd)

        if not (len(gcd) == 1 and gcd[0] == 1):
            return False

        i += 1

    # Step 3: Check if f | (X^(p^n) - X)
    g = __pow_poly(p, n)
    _, _, gcd = egcd.egcd(f, g, p)
    gcd = remove_degree(gcd)

    # Check if gcd == f (meaning f divides g)
    if i == k and gcd == f:
        return True

    return False


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
    f = random.choices(range(p), k=n + 1)
    while f[-1] == 0:
        f[-1] = random.randint(1, p - 1)
    return f


def __pow_poly(p: int, n: int) -> list[int]:
    """
    Returns polynomial X^q^t - X
    """
    d = pow(p, n)
    g = [0 for _ in range(d + 1)]
    g[-1] = 1
    g[1] = p - 1
    return g


def __prime_divisors(n: int) -> list[int]:
    """
    Returns list of prime divisors of n
    """
    if n <= 1:
        return []

    primes: list[int] = []

    for i in range(2, n // 2 + 1):
        if n % i == 0:
            primes.append(i)
            while n % i == 0:
                n //= i

        if n == 1:
            break

    if n > 1:
        primes.append(n)

    return primes
