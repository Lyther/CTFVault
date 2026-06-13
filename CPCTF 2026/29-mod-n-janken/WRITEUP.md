# mod N Janken

## Setup

- 100 NPCs each have a 120-element strategy `[s, M(s), M^2(s), ..., M^119(s)]` where `M` is the xorshift64 step `n ← n^(n<<13) ; n ← n^(n>>7) ; n ← n^(n<<17)` (truncated to 64 bits at the end). `M` is GF(2)-linear.
- We supply our own 120-value strategy `P_j` (any 64-bit ints) as the 101st participant.
- Per match: random `player_no ∈ {0..100}`, random 120-bit `luck`. We may flip up to 600 luck bits across 20 matches. After flips, `clash = ⊕_{i,j} strat[i][j] · luck[j]`, and we win iff `clash mod 101 == player_no`.

## Algebra

Let `T = ⊕_i seed_i` (one unknown 64-bit constant). Linearity of `M` gives `⊕_i strat[i][j] = M^j · T`. So

```text
clash = M_S · T  ⊕  K_S
```

where `S = {j : luck[j] = 1}`, `M_S = ⊕_{j∈S} M^j`, `K_S = ⊕_{j∈S} P_j`.

Picking `S` so `M_S = 0` kills the unknown `T` term. Among `M^0..M^119` only 64 are linearly independent (xorshift64 with shifts 13/7/17 has min-poly degree 64 = full period 2^64−1), so the **kernel has dimension 56**. For any `S` in that kernel `clash = K_S` is fully under our control.

## Per-match decoding

1. Compute `H` (64×120 parity-check) for the kernel by Gaussian elimination on the 4096×120 system `Σ x_j · vec(M^j) = 0`.
2. For luck `L`: compute syndrome `s = H · L`. Need `y` with `H·y = s`, low Hamming weight, and `K_{L⊕y} mod 101 = player_no`.
3. ISD-Prange + Lee-Brickell `p=2`:
   - Random column permutation, Gauss-eliminate to systematic form `[I | H']`.
   - For each `(j, k)` over the 56 free columns, candidate is `y_basic = s' ⊕ D[j] ⊕ D[k]`, weight `popcount(...) + 2`. Check mod-101.
   - ~200 trials × 1+56+1540 candidates → average ~21 flips per match, well under the 30/match budget.

## Critical bug I hit (and the fix)

Server's `nextrand` does **not** mask after each shift:

```python
n ^= n << 13
n ^= n >> 7
n ^= n << 17
return n & ((1 << 64) - 1)
```

In Python's arbitrary-precision int the `n << 13` overflow bits survive and feed back into the low 64 bits via `n >> 7`. So the canonical "masked" xorshift64 produces a **different** matrix `M`. Local kernel decoding looked correct (assertion `K(P, x_S) % 101 == player_no` passed) but the actual server clash mismatched because the server's `M^j` are not what I had been computing. Replacing my `xorshift64` with the byte-for-byte equivalent of `nextrand` fixes the kernel and everything works.

## Result

```text
CPCTF{Tie_15_A_T1Me_ThiEf}
```

Total cheats used: 421/600 (~21 per match).
