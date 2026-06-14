# Matemith — Writeup

- Category:
- Value: 500

## Challenge

> <p>Solving <a href="/tasks/matemith_68a21bacc713364e8665937e40caa12114d82667.txz"><strong>Matemith’s</strong></a> polynomial equations is easier than pronouncing ‘Matemith’, but that’s not saying much!</p>

## Flag

```text
CCTF{50lv!n6_7H3_H1dD3n__num8Ers_Pr08l3m_f0r_C51dH_4nd_C5uRf_v14_4uT0m473d_C0pp3r5m17h!!?}
```

## Recon

The flag is stripped of `CCTF{}` and split into six 14-byte chunks, which are
the variables `u, v, w, x, y, z` in the published polynomial equations over the
prime field `GF(p)`.  We get six equations:

- `f` is bilinear in `u, v`
- `g` is trilinear in `u, x, y` plus a `v` term
- `h` is bilinear in `u, w`
- `i` is trilinear in `v, y, z` plus `w`/`y`/`z` terms
- `j` is bilinear in `v, w`
- `k` is trilinear in `w, x, z` plus `u`/`x`/`z` terms

## Solve

1. From `f` and `h`, express `v` and `w` rationally in terms of `u`.
2. Substitute these into `j` to obtain a quadratic in `u` over `GF(p)`.  Solve
   it with Tonelli–Shanks.
3. For each candidate `u`, compute the corresponding `v` and `w`.
4. Substitute those into `g`, `i`, `k`; the remaining unknowns are `x, y, z`.
   Compute a lexicographic Gröbner basis over `GF(p)`, which yields a linear
   system in `x` and `y` plus a quadratic in `z`.
5. Solve the quadratic for `z`, recover `x` and `y`, and verify all six
   equations.
6. Reassemble the six 14-byte chunks into the flag.
