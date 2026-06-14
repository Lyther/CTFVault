#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Solve Interpol (Crypto CTF 2026).

The challenge dumps a Sage QQ[x] Lagrange interpolation polynomial.  The
interpolation data contains:
- L true flag points with negative x and integer y.
- c random points with x in [0, 313] and rational y = +/- p/q.

Only the negative x-values belong to the flag, so we evaluate the recovered
polynomial at those x-values, decode the y-values as ASCII, and place each
character at position (63*n - 40) mod L.
"""

import pickle
import sys
import types
import zlib
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHALLENGE = (
    HERE.parent / "files" / "24_interpol_294c02588bda413403f6ded64c62bcd73f75435e.txz"
)


def _install_sage_stubs() -> None:
    """Provide minimal stand-ins for the Sage classes used by the pickle."""
    sage = types.ModuleType("sage")
    sage.rings = types.ModuleType("sage.rings")
    sage.rings.polynomial = types.ModuleType("sage.rings.polynomial")
    sage.rings.polynomial.polynomial_rational_flint = types.ModuleType(
        "sage.rings.polynomial.polynomial_rational_flint",
    )
    sage.rings.polynomial.polynomial_ring_constructor = types.ModuleType(
        "sage.rings.polynomial.polynomial_ring_constructor",
    )
    sage.rings.rational_field = types.ModuleType("sage.rings.rational_field")
    sage.rings.rational = types.ModuleType("sage.rings.rational")
    sage.structure = types.ModuleType("sage.structure")
    sage.structure.parent = types.ModuleType("sage.structure.parent")

    class _Parent:
        pass

    sage.structure.parent.Parent = _Parent

    class _QQ:
        def __repr__(self) -> str:
            return "QQ"

    class _PolynomialRing:
        def __init__(self, base_ring, names=("x",), **kwargs) -> None:
            self.base_ring = base_ring
            self.names = names

    class _PolynomialRationalFlint:
        def __init__(self, parent, coeffs) -> None:
            self.parent = parent
            # coefficients in ascending order: c0 + c1*x + ... + cd*x^d
            self.coeffs = coeffs

        def __call__(self, x: int) -> Fraction:
            res: Fraction = Fraction(0)
            for coeff in reversed(self.coeffs):
                res = res * x + coeff
            return res

    def _make_rational(s: bytes | str) -> Fraction:
        if isinstance(s, bytes):
            s = s.decode("ascii")
        s = s.strip()
        sign = -1 if s.startswith("-") else 1
        if sign == -1:
            s = s[1:]
        if "/" in s:
            num, den = s.split("/")
            return sign * Fraction(int(num, 32), int(den, 32))
        return sign * Fraction(int(s, 32), 1)

    def _unpickle_PolynomialRing(
        base_ring,
        names,
        order=None,
        is_sparse=False,
        **kwargs,
    ):
        if isinstance(names, str):
            names = (names,)
        return _PolynomialRing(base_ring, names=names)

    def _poly_new(cls, *args) -> _PolynomialRationalFlint:
        return _PolynomialRationalFlint(args[0], args[1] if len(args) > 1 else [])

    sage.rings.polynomial.polynomial_rational_flint.Polynomial_rational_flint = type(
        "Polynomial_rational_flint",
        (),
        {"__new__": _poly_new},
    )
    sage.rings.polynomial.polynomial_ring_constructor.unpickle_PolynomialRing = (
        _unpickle_PolynomialRing
    )
    sage.rings.rational.make_rational = _make_rational
    sage.rings.rational_field.RationalField = _QQ
    sage.rings.rational_field.QQ = _QQ()

    for name, mod in (
        ("sage", sage),
        ("sage.rings", sage.rings),
        ("sage.rings.polynomial", sage.rings.polynomial),
        (
            "sage.rings.polynomial.polynomial_rational_flint",
            sage.rings.polynomial.polynomial_rational_flint,
        ),
        (
            "sage.rings.polynomial.polynomial_ring_constructor",
            sage.rings.polynomial.polynomial_ring_constructor,
        ),
        ("sage.rings.rational_field", sage.rings.rational_field),
        ("sage.rings.rational", sage.rings.rational),
        ("sage.structure", sage.structure),
        ("sage.structure.parent", sage.structure.parent),
    ):
        sys.modules[name] = mod


def _extract_output_raw() -> bytes:
    import lzma
    import tarfile

    with lzma.open(CHALLENGE, "r") as tar_bytes:
        with tarfile.open(fileobj=tar_bytes, mode="r:") as tar:
            member = tar.getmember("interpol/output.raw")
            return tar.extractfile(member).read()


def _load_polynomial(raw: bytes):
    _install_sage_stubs()
    decompressed = zlib.decompress(raw)
    return pickle.loads(decompressed)


def recover_flag(poly) -> str:
    degree = len(poly.coeffs) - 1
    max_len = degree + 1

    for flag_len in range(10, max_len + 1):
        chars: list[str | None] = [None] * flag_len
        ok = True
        for n in range(flag_len):
            x = -(1 + (19 * n - 14) % flag_len)
            y = poly(x)
            if y.denominator != 1:
                ok = False
                break
            value = int(y)
            if not (32 <= value <= 126):
                ok = False
                break
            pos = (63 * n - 40) % flag_len
            if chars[pos] is None:
                chars[pos] = chr(value)
            elif chars[pos] != chr(value):
                ok = False
                break
        if ok and None not in chars:
            flag = "".join(chars)
            if "CCTF" in flag:
                return flag
    raise RuntimeError("flag not recovered")


def main() -> None:
    raw = _extract_output_raw()
    poly = _load_polynomial(raw)
    flag = recover_flag(poly)
    print(flag)


if __name__ == "__main__":
    main()
