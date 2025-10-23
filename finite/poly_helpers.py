# module with polynomial arithmetic helpers for finite field operations

from polynomial.add_sub import add as poly_add, sub as poly_sub
import random

def poly_mult(f: list[int], g: list[int], p: int) -> list[int]:
    """
    Multiplies f by g and returns result in Z_p[X]
    """
    if (len(f) == 1 and f[0] == 0) or (len(g) == 1 and g[0] == 0):
        return [0]
    
    deg_f = len(f) - 1
    deg_g = len(g) - 1
    deg_res = deg_f + deg_g
    res = [0] * (deg_res + 1)

    for i in range(len(f)):
        for j in range(len(g)):
            res[i+j] = (res[i+j] + f[i] * g[j]) % p
    
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    if not res:
        res = [0]
        
    return res

def poly_long_div(f: list[int], g: list[int], p: int) -> tuple[list[int] | None, list[int] | None]:
    """
    Divides f by g in Z_p[X] and returns q, r (in this order) such that
    f = q * g + r
    """
    if not g or (len(g) == 1 and g[0] == 0):
        return None, None

    if len(f) == 1 and f[0] == 0:
        return [0], [0]

    deg_f = len(f) - 1
    deg_g = len(g) - 1

    if deg_f < deg_g:
        return [0], f

    q = [0] * (deg_f - deg_g + 1)
    rem = f[:]

    if g[-1] == 0:
        return None, None
    lc_g_inv = pow(g[-1], -1, p)

    for i in range(deg_f - deg_g, -1, -1):
        if len(rem) <= i + deg_g or rem[i + deg_g] == 0:
            continue
        coeff = (rem[i + deg_g] * lc_g_inv) % p
        q[i] = coeff
        for j in range(deg_g + 1):
            rem[i + j] = (rem[i + j] - coeff * g[j]) % p

    while len(rem) > 1 and rem[-1] == 0:
        rem.pop()
    if not rem:
        rem = [0]

    return q, rem

def poly_egcd(f: list[int], g: list[int], p: int) -> tuple[list[int] | None, list[int] | None, list[int] | None]:
    """
    Finds a, b, d such that:
    a * f + b * g = d, in Z_p[X],
    where d = gcd(f, g) is monic
    and returns a, b, d (in this order)
    """
    if (len(f) == 1 and f[0] == 0):
        if not g or (len(g) == 1 and g[0] == 0): return [1], [0], [0]
        lc_g_inv = pow(g[-1], -1, p)
        d = poly_mult(g, [lc_g_inv], p)
        return [0], [lc_g_inv], d

    old_r, r = f, g
    old_s, s = [1], [0]
    old_t, t = [0], [1]

    while not (len(r) == 1 and r[0] == 0):
        q, rem = poly_long_div(old_r, r, p)
        if q is None:
            return None, None, None

        old_r, r = r, rem
        
        s_new = poly_sub(old_s, poly_mult(q, s, p), p)
        if not s_new: s_new = [0]
        old_s, s = s, s_new

        t_new = poly_sub(old_t, poly_mult(q, t, p), p)
        if not t_new: t_new = [0]
        old_t, t = t, t_new

    d = old_r
    a = old_s
    b = old_t
    
    if not d or (len(d) == 1 and d[0] == 0):
        return [1], [0], [0]

    lc_d_inv = pow(d[-1], -1, p)
    
    d = poly_mult(d, [lc_d_inv], p)
    a = poly_mult(a, [lc_d_inv], p)
    b = poly_mult(b, [lc_d_inv], p)

    return a, b, d

def get_prime_factors(n):
    factors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return list(factors)

def poly_pow(base, exp, mod, p):
    res = [1]
    _, base_rem = poly_long_div(base, mod, p)
    if base_rem is None: base_rem = base

    while exp > 0:
        if exp % 2 == 1:
            res = poly_mult(res, base_rem, p)
            _, res = poly_long_div(res, mod, p)
        base_rem = poly_mult(base_rem, base_rem, p)
        _, base_rem = poly_long_div(base_rem, mod, p)
        exp //= 2
    return res
