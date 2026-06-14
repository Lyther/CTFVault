#!/usr/bin/env python3
"""
Solve Mancity (Crypto CTF 2026 #20).

Keygen builds a 256-bit prime p and two derived primes:
    q = (p << 256) | (2**256 - 1)        # p's bits followed by 256 ones
    r = man(p)                           # bit-doubled version of p
The modulus is n = q * r.

Both q and r have a very sparse algebraic description in terms of p's bits,
so n is a polynomial-ish product. We recover p bit-by-bit with a Hensel-lifting
style iteration: at each bit position t we know the contribution of the lower
bits already fixed, and the new bits of q/r are linear functions of a single
unknown p-bit (or constant). This makes every bit of p recoverable directly
from n, with O(N) big-integer work for N=256.
"""

from pathlib import Path

from Crypto.Util.number import inverse, isPrime, long_to_bytes

N = 256
E = 1234567891

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "files" / "Mancity" / "output.txt"
FLAG_FILE = ROOT / "solution" / "flag.txt"


def man(num: int) -> int:
    """Bit-doubling map used in the challenge."""
    bits = bin(num)[2:]
    out = ""
    for bit in bits:
        out += "01" if bit == "0" else "11"
    return int(out, 2)


def recover_p(n: int, nbit: int) -> int:
    """Recover the secret prime p from n = q*r.

    Let p_i be bit i of p (i=0 LSB, i=nbit-1 MSB). Then
        q_i = 1                  for 0 <= i < nbit
        q_{nbit+i} = p_i         for 0 <= i < nbit
        r_{2i}   = 1             for 0 <= i < nbit
        r_{2i+1} = p_i           for 0 <= i < nbit

    We build P (q) and Q (r) incrementally. At step t the already fixed lower
    bits of P and Q multiply to a known partial product; the new bits contribute
    pt and qt, and the bit equation is
        n_t = (P*Q >> t)&1 XOR pt XOR qt   (mod 2)
    Because at most one of pt/qt depends on an unknown p-bit, the unknown bit
    is determined immediately. The MSB p_{nbit-1} is forced to 1 because p is
    an nbit-bit prime.
    """
    pbits = [None] * nbit
    pbits[nbit - 1] = 1

    partial_p = 1  # lower bits of q constructed so far
    partial_q = 1  # lower bits of r constructed so far

    if (n & 1) != 1:
        raise ValueError("n must be odd")

    for t in range(1, 4 * nbit + 1):
        carry = ((partial_p * partial_q) >> t) & 1
        nt = (n >> t) & 1

        if t < nbit:
            # q_t = 1, r_t = p_{(t-1)/2} when t odd; both 1 when t even
            if t % 2 == 0:
                if carry != nt:
                    raise ValueError(f"low even bit {t} inconsistent")
            else:
                pbits[(t - 1) // 2] = nt ^ carry ^ 1

        elif t < 2 * nbit:
            if t % 2 == 0:
                # q_t = p_{t-nbit}, r_t = 1
                pbits[t - nbit] = nt ^ carry ^ 1
            else:
                # q_t = p_{t-nbit}, r_t = p_{(t-1)/2}
                new_idx = t - nbit
                old_idx = (t - 1) // 2
                if new_idx == old_idx:
                    # t = 2*nbit - 1, both are the forced MSB; equation is 0 = nt ^ carry
                    if (nt ^ carry) != 0:
                        raise ValueError(f"MSB relation at {t} inconsistent")
                elif pbits[old_idx] is None:
                    # old bit not yet known: solve for it from the new one
                    if pbits[new_idx] is None:
                        raise ValueError(f"unsolvable relation at {t}")
                    pbits[old_idx] = nt ^ carry ^ pbits[new_idx]
                else:
                    pbits[new_idx] = nt ^ carry ^ pbits[old_idx]
        elif carry != nt:
            raise ValueError(f"upper bit {t} inconsistent")

        # Update the partial products with the bits just determined.
        if t < 2 * nbit:
            if t < nbit:
                pt = 1
                qt = pbits[(t - 1) // 2] if t % 2 == 1 else 1
            else:
                pt = pbits[t - nbit]
                qt = 1 if t % 2 == 0 else pbits[(t - 1) // 2]

            if pt is None or qt is None:
                continue
            partial_p |= pt << t
            partial_q |= qt << t

    if any(b is None for b in pbits):
        raise ValueError("not all bits of p were recovered")

    return sum(b << i for i, b in enumerate(pbits))


def main() -> None:
    raw = OUTPUT.read_text()
    n = int(raw.split("n = ")[1].splitlines()[0])
    c = int(raw.split("c = ")[1].splitlines()[0])

    p = recover_p(n, N)
    q = (p << N) | ((1 << N) - 1)
    r = man(p)

    assert q * r == n, "recovered modulus mismatch"
    assert isPrime(p) and isPrime(q) and isPrime(r), "recovered factors not prime"

    phi = (q - 1) * (r - 1)
    d = inverse(E, phi)
    m = pow(c, d, n)
    flag = long_to_bytes(m)

    FLAG_FILE.write_bytes(flag)
    print(flag.decode())


if __name__ == "__main__":
    main()
