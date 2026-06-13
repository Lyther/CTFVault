# Vinad — Writeup

- Category:
- Value: 500

## Challenge

> <p><a href="/tasks/Vinad_9c347fb64604b79eda25a6b2216b292014f38333.txz">Vinad's</a> ‘random’ keys are as unpredictable as a cat. Poke its weak spots, steal the flag—chaos included!</p>

## Flag

```text
CCTF{s0lV1n9_4_Syst3m_0f_L1n3Ar_3qUaTi0n5_0vEr_7H3_F!3lD_F(2)!}
```

## Recon

The `vinad` function constructs integers by computing parity bits: each output bit `i` equals `parinad(x XOR R[i]) = popcount(x) % 2 XOR popcount(R[i]) % 2`. This means `vinad(x, R)` is linear over GF(2): bit `i = b XOR a_i` where `b = parinad(x)` and `a_i = parinad(R[i])`.

Since R is public, we compute `a_i` for all 512 entries and build the integer `A`. The prime `p = vinad(r, R)` has bits `p_i = b XOR a_i`, so `p` is either `A` (if `b=0`) or the bitwise complement of `A` within 512 bits (if `b=1`).

## Solve

1. Compute `a_i = parinad(R[i])` for all `i`, build integer `A` from these bits.
2. Try `p = A` and `p = A XOR (2^512 - 1)`; check if `n % p == 0`.
3. With `p` found, compute `q = n // p`, `phi = (p-1)(q-1)`.
4. Since `e` shares the same `a_i` vector as `p` (bits differ by at most a constant), try `e = p` and `e = p XOR (2^512-1)`; pick the one coprime to `phi`.
5. Compute `d = e^{-1} mod phi`, decrypt: `m = pow(c, d, n) - sum(R) mod n`.
6. Convert `m` to bytes → flag.
