#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "sympy",
# ]
# ///

"""Solve Matemith (Crypto CTF 2026).

The challenge splits the flag into six 14-byte chunks M0..M5 and provides six
multivariate equations over GF(p) satisfied by (M0..M5).  We solve by
substituting the linear/bilinear equations to reduce to one variable, then
use a Groebner basis for the remaining three variables.
"""

from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
CHALLENGE = (
    HERE.parent / "files" / "36_matemith_68a21bacc713364e8665937e40caa12114d82667.txz"
)


def _extract_output(tmp: Path) -> Path:
    import tarfile

    out = tmp / "matemith"
    if not out.is_dir():
        with tarfile.open(CHALLENGE, "r:xz") as tf:
            tf.extractall(tmp)
    return out / "output.txt"


def _parse_output(path: Path) -> tuple[int, list[sp.Poly]]:
    text = path.read_text()
    lines = text.splitlines()
    p = int(lines[0].split("=", 1)[1].strip())
    u, v, w, x, y, z = sp.symbols("u v w x y z")

    def parse(line: str) -> sp.Poly:
        expr_str = line.split("=", 1)[1].strip()
        expr = 0
        for mon in expr_str.split("+"):
            terms = [t.strip() for t in mon.split("*")]
            coef = int(terms[0])
            mon_expr = coef
            for var in terms[1:]:
                mon_expr *= sp.symbols(var)
            expr += mon_expr
        return sp.Poly(expr, u, v, w, x, y, z, domain=sp.GF(p))

    polys = [parse(line) for line in lines[1:] if "=" in line]
    return p, polys


def _to_int_expr(P: sp.Poly) -> sp.Expr:
    expr = 0
    u, v, w, x, y, z = sp.symbols("u v w x y z")
    gens = [u, v, w, x, y, z]
    for mon, coeff in zip(P.monoms(), P.coeffs()):
        term = int(coeff)
        for i, exp in enumerate(mon):
            if exp:
                term *= gens[i] ** exp
        expr += term
    return expr


def _tonelli(n: int, p: int) -> int:
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    c = pow(z, q, p)
    x0 = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    while t != 1:
        i = 1
        while pow(t, 2**i, p) != 1:
            i += 1
        b_ = pow(c, 2 ** (m - i - 1), p)
        x0 = x0 * b_ % p
        t = t * b_ * b_ % p
        c = b_ * b_ % p
        m = i
    return x0


def solve(path: Path) -> str:
    p, polys = _parse_output(path)
    P0, P1, P2, P3, P4, P5 = polys

    def coeff(P: sp.Poly, mon: tuple[int, ...]) -> int:
        try:
            return int(P.coeff_monomial(mon))
        except Exception:
            return 0

    def inv(a: int) -> int:
        return pow(a, -1, p)

    c0 = coeff(P0, (1, 1, 0, 0, 0, 0))
    c1 = coeff(P0, (1, 0, 0, 0, 0, 0))
    c2 = coeff(P0, (0, 1, 0, 0, 0, 0))
    cf = coeff(P0, (0, 0, 0, 0, 0, 0))

    c7 = coeff(P2, (1, 0, 1, 0, 0, 0))
    c8 = coeff(P2, (0, 0, 1, 0, 0, 0))
    c9 = coeff(P2, (1, 0, 0, 0, 0, 0))
    ch = coeff(P2, (0, 0, 0, 0, 0, 0))

    c14 = coeff(P4, (0, 1, 1, 0, 0, 0))
    c15 = coeff(P4, (0, 1, 0, 0, 0, 0))
    c16 = coeff(P4, (0, 0, 1, 0, 0, 0))
    cj = coeff(P4, (0, 0, 0, 0, 0, 0))

    U = sp.symbols("U")

    # Eliminate v and w from f and h, leaving a quadratic in u from j.
    j_num = (
        c14 * (-(c1 * U + cf)) * (-(c9 * U + ch))
        + c15 * (-(c1 * U + cf)) * (c7 * U + c8)
        + c16 * (-(c9 * U + ch)) * (c0 * U + c2)
        + cj * (c0 * U + c2) * (c7 * U + c8)
    )
    j_poly = sp.Poly(
        sum(
            (int(t.as_coeff_mul(U)[0]) % p) * sp.Mul(*t.as_coeff_mul(U)[1])
            for t in sp.expand(j_num).as_ordered_terms()
        ),
        U,
        domain=sp.GF(p),
    )
    a, b, c = [int(co) for co in j_poly.all_coeffs()]
    disc = (b * b - 4 * a * c) % p
    if pow(disc, (p - 1) // 2, p) != 1:
        raise RuntimeError("j quadratic has no roots")

    sqrt_disc = _tonelli(disc, p)
    inv2a = inv(2 * a)

    for sign in (1, -1):
        U0 = (-b + sign * sqrt_disc) * inv2a % p
        if (c0 * U0 + c2) % p == 0 or (c7 * U0 + c8) % p == 0:
            continue
        v0 = (-(c1 * U0 + cf)) * inv(c0 * U0 + c2) % p
        w0 = (-(c9 * U0 + ch)) * inv(c7 * U0 + c8) % p

        # Remaining equations in x, y, z after substituting known u, v, w.
        P1_sub = sp.Poly(
            _to_int_expr(P1).subs({sp.symbols("u"): U0, sp.symbols("v"): v0}),
            sp.symbols("x"),
            sp.symbols("y"),
            domain=sp.GF(p),
        )
        P3_sub = sp.Poly(
            _to_int_expr(P3).subs({sp.symbols("v"): v0, sp.symbols("w"): w0}),
            sp.symbols("y"),
            sp.symbols("z"),
            domain=sp.GF(p),
        )
        P5_sub = sp.Poly(
            _to_int_expr(P5).subs({sp.symbols("u"): U0, sp.symbols("w"): w0}),
            sp.symbols("x"),
            sp.symbols("z"),
            domain=sp.GF(p),
        )

        x, y, z = sp.symbols("x y z")
        G = sp.groebner(
            [P1_sub.as_expr(), P3_sub.as_expr(), P5_sub.as_expr()],
            x,
            y,
            z,
            modulus=p,
        )

        Pz = sp.Poly(G[-1], z, domain=sp.GF(p))
        a2, b1, c0c = [int(Pz.coeff_monomial((i,))) for i in (2, 1, 0)]
        disc_z = (b1 * b1 - 4 * a2 * c0c) % p
        if pow(disc_z, (p - 1) // 2, p) != 1:
            continue
        sz = _tonelli(disc_z, p)
        inv2a2 = inv(2 * a2)

        Pxy = sp.Poly(G[0], x, z, domain=sp.GF(p))
        Pzy = sp.Poly(G[1], y, z, domain=sp.GF(p))
        a_x = int(Pxy.coeff_monomial((1, 0)))
        b_x = int(Pxy.coeff_monomial((0, 1)))
        c_x = int(Pxy.coeff_monomial((0, 0)))
        a_y = int(Pzy.coeff_monomial((1, 0)))
        b_y = int(Pzy.coeff_monomial((0, 1)))
        c_y = int(Pzy.coeff_monomial((0, 0)))

        for z_sign in (1, -1):
            Z = (-b1 + z_sign * sz) * inv2a2 % p
            X = (-b_x * Z - c_x) * inv(a_x) % p
            Y = (-b_y * Z - c_y) * inv(a_y) % p

            vals = (U0, v0, w0, X, Y, Z)
            ok = True
            for P in polys:
                val = 0
                for mon, coeff in zip(P.monoms(), P.coeffs()):
                    term = int(coeff)
                    for i, exp in enumerate(mon):
                        if exp:
                            term = (term * pow(vals[i], exp, p)) % p
                    val = (val + term) % p
                if val != 0:
                    ok = False
                    break
            if ok:
                inner = b"".join(vv.to_bytes(14, "big") for vv in vals)
                flag = b"CCTF{" + inner + b"}"
                return flag.decode()
    raise RuntimeError("flag not recovered")


def main() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = _extract_output(Path(tmp))
        flag = solve(out)
    print(flag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
