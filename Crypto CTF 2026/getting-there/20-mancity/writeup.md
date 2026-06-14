# Mancity — Writeup

- Category: Crypto
- Value: 500

## Challenge

> <p>Decipher <a href="/tasks/Mancity_2a14c2969c2872883e6e78a3481cbcd8f0bdf318.txz"><strong>Mancity</strong></a> by exploiting RSA modulus secrets, bit by bit, relation by relation.</p>

## Flag

```text
CCTF{M4nch3sReR_c0D!ng_wI7H_RSA}
```

## Solve

The challenge key generation derives two primes from a single secret 256-bit prime `p`:

- `q = (p << 256) | (2**256 - 1)` — the bits of `p` followed by 256 ones.
- `r = man(p)` — each bit of `p` is doubled (`0 -> 01`, `1 -> 11`).

The RSA modulus is `n = q * r`. Because both factors are simple functions of the same `p`, every bit of `n` gives a linear equation in one (or a relation between two) bits of `p`. We recover `p` bit-by-bit with a Hensel-lifting style iteration:

1. Maintain the partial products of the already fixed lower bits of `q` and `r`.
2. At bit position `t`, the new contributions are known linear functions of at most one unknown `p`-bit, plus a known carry.
3. Equate to the corresponding bit of `n` and solve for the unknown `p`-bit.

The MSB `p_255` is forced to `1` because `p` is a 256-bit prime. Once `p` is recovered, `q` and `r` follow directly, allowing a normal RSA decryption.

See `scripts/solve.py` for the full implementation.
