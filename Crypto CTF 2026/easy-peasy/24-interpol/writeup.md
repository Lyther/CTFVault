# Interpol — Writeup

- Category: Easy-Peasy 🍰
- Value: 500

## Challenge

> <p>Only brute force won't crack <a href="/tasks/interpol_294c02588bda413403f6ded64c62bcd73f75435e.txz"><strong>Interpol</strong></a>! Its massive polynomial guards the flag fiercely.</p>

## Recon

`interpol/interpol.sage` builds a Lagrange polynomial over `QQ[x]` from two kinds of points:

1. **Flag points** (added when the `randint(0,1)` coin flip is `1`):
   - `x = -(1 + (19*n - 14) % len(flag))`
   - `y = ord(flag[(63*n - 40) % len(flag)])`

2. **Random points** (added when the coin flip is `0`):
   - `x = randint(0, 313)`
   - `y = ±p/q` with `p, q` random 32-bit primes

Only the flag points have **negative** `x` values, so evaluating the polynomial at those `x` values gives ASCII ordinals. The polynomial is then dumped to `output.raw`.

## Solve

`output.raw` is a zlib-compressed Sage pickle of a `Polynomial_rational_flint`. The rational coefficients are base32 strings passed through `sage.rings.rational.make_rational`.

Since SageMath is not installed locally, the solver registers minimal stub modules (`sage.rings.polynomial.polynomial_rational_flint`, `sage.rings.rational.make_rational`, etc.) so Python's `pickle` can reconstruct the polynomial as a plain list of `Fraction` coefficients.

Then, for every candidate flag length `L` from `10` up to the number of interpolation points, the solver:

1. Evaluates the polynomial at the negative flag x-values.
2. Checks that each result is an integer in `[32, 126]`.
3. Places the decoded character at position `(63*n - 40) % L`.
4. Returns the first result containing `CCTF{...}`.

```bash
uv run scripts/solve.py
```

## Flag

```text
CCTF{7h3_!nTeRn4t10naL_Cr!Min41_pOlIc3_0r9An!Zati0n!}
```
