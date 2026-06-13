#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pycryptodome",
#   "sympy",
# ]
# ///

import hashlib
import pathlib
import re
from fractions import Fraction
from math import comb

from Crypto.Cipher import AES
from sympy import ZZ, Poly, symbols

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "4_output.txt"
LOW_BITS = 72
LATTICE_M = 3
LATTICE_T = 2


def parse_output() -> dict[str, str]:
    text = CHALLENGE.read_text(encoding="utf-8")
    return dict(re.findall(r"^(\w+) = ([^\r\n]+)", text, re.MULTILINE))


def nearest_integer(value: Fraction) -> int:
    numerator = value.numerator
    denominator = value.denominator
    if numerator >= 0:
        return (2 * numerator + denominator) // (2 * denominator)
    return -((2 * (-numerator) + denominator) // (2 * denominator))


def gram_schmidt(basis: list[list[int]]) -> tuple[list[list[Fraction]], list[Fraction]]:
    rows = len(basis)
    cols = len(basis[0])
    orthogonal = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    mu = [[Fraction(0) for _ in range(rows)] for _ in range(rows)]
    norms = [Fraction(0) for _ in range(rows)]

    for i, row in enumerate(basis):
        vector = [Fraction(value) for value in row]
        for j in range(i):
            mu[i][j] = (
                sum(Fraction(row[k]) * orthogonal[j][k] for k in range(cols)) / norms[j]
            )
            for k in range(cols):
                vector[k] -= mu[i][j] * orthogonal[j][k]
        orthogonal[i] = vector
        norms[i] = sum(value * value for value in vector)

    return mu, norms


def lll_reduce(basis: list[list[int]]) -> list[list[int]]:
    reduced = [row[:] for row in basis]
    delta = Fraction(3, 4)
    mu, norms = gram_schmidt(reduced)
    k = 1

    while k < len(reduced):
        changed = False
        for j in range(k - 1, -1, -1):
            q = nearest_integer(mu[k][j])
            if q:
                reduced[k] = [
                    value - q * reduced[j][i] for i, value in enumerate(reduced[k])
                ]
                changed = True
        if changed:
            mu, norms = gram_schmidt(reduced)

        if norms[k] >= (delta - mu[k][k - 1] * mu[k][k - 1]) * norms[k - 1]:
            k += 1
            continue

        reduced[k], reduced[k - 1] = reduced[k - 1], reduced[k]
        mu, norms = gram_schmidt(reduced)
        k = max(k - 1, 1)

    return reduced


def build_lattice(modulus: int, known_high: int, bound: int) -> list[list[int]]:
    dimension = LATTICE_M + LATTICE_T
    rows = []

    for i in range(LATTICE_M):
        row = [0] * dimension
        for k in range(i + 1):
            row[k] = (
                comb(i, k)
                * known_high ** (i - k)
                * bound**k
                * modulus ** (LATTICE_M - i)
            )
        rows.append(row)

    for i in range(LATTICE_T):
        row = [0] * dimension
        for j in range(LATTICE_M + 1):
            row[i + j] = (
                comb(LATTICE_M, j) * known_high ** (LATTICE_M - j) * bound ** (i + j)
            )
        rows.append(row)

    return rows


def recover_low_bits(modulus: int, known_high: int, bound: int) -> int:
    x = symbols("x")
    reduced = lll_reduce(build_lattice(modulus, known_high, bound))
    reduced.sort(key=lambda row: sum(value * value for value in row))

    for row in reduced:
        coeffs = [row[i] // bound**i for i in range(len(row))]
        poly = Poly.from_list(list(reversed(coeffs)), gens=x, domain=ZZ)
        for root in poly.ground_roots():
            candidate = int(root)
            if 0 <= candidate < bound and modulus % (known_high + candidate) == 0:
                return candidate

    raise ValueError("failed to recover p low bits")


def long_to_bytes(value: int) -> bytes:
    return value.to_bytes((value.bit_length() + 7) // 8 or 1, "big")


def main() -> None:
    values = parse_output()
    modulus = int(values["N"])
    exponent = int(values["e"])
    bound = 1 << LOW_BITS
    known_high = int(values["p_hi"]) * bound
    low = recover_low_bits(modulus, known_high, bound)
    p = known_high + low
    q = modulus // p
    phi = (p - 1) * (q - 1)
    private_exponent = pow(exponent, -1, phi)
    key = hashlib.sha256(long_to_bytes(private_exponent)).digest()[:16]
    cipher = AES.new(key, AES.MODE_GCM, nonce=bytes.fromhex(values["nonce"]))
    flag = cipher.decrypt_and_verify(
        bytes.fromhex(values["ciphertext"]),
        bytes.fromhex(values["tag"]),
    )
    print(flag.decode())


if __name__ == "__main__":
    main()
