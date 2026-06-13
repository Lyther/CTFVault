# RPS Eliminations (Yukicoder No. 3510)

Let the given eliminations define a full ordered binary tree on the original `N` positions.

- Each leaf is one initial character.
- At step `i`, the current segments at positions `A_i` and `A_i+1` are merged.
- The merged segment becomes their parent.

So the whole process is just evaluating this tree bottom-up by rock-paper-scissors.

For a node `v`, define `F(v, c)` as the set of strings on the leaves of `v` whose winner becomes `c`.

- Leaf: `F(leaf, c) = { c }`
- Internal node with children `L, R`:

```text
F(v, c)
= F(L, c) concat F(R, loser(c))
  union
  F(L, loser(c)) concat F(R, c)
```

because the two child winners must be different, and the parent winner is the stronger one.

The key induction fact is that `F(v, P)`, `F(v, R)`, `F(v, S)` are pairwise disjoint for every node `v`.
That means a fixed left substring determines its winner label uniquely.

This allows a lexicographic selection DP without merging huge implicit sorted lists.

Use a generalized routine:

```text
solve(v, W, k)
```

Here `W[c]` means:

- every string in `F(v, c)` represents a block of `W[c]` suffix choices,
- and we want the `k`-th string in lexicographic order over all those blocks.

At a leaf, just choose among `P < R < S` by cumulative block sizes.

At an internal node:

1. Suppose the left winner is `d`.
2. Then the right winner can come from:
   - parent winner `d`, which forces right winner `loser(d)`
   - parent winner `beat(d)`, which forces right winner `beat(d)`
3. So we get a right-side weight vector `RW_d`.
4. Every left string in `F(L, d)` has the same block size:

```text
BW[d] = total_weight(R, RW_d)
```

5. First recurse into the left child with weights `BW` to determine:
   - which left winner `d` was chosen,
   - and which offset inside that block remains.
6. Then recurse into the right child with `RW_d` and that offset.

The answer string is produced by this recursion directly on the leaves.

## Building the tree

Simulate the merges with a Fenwick tree over the current alive positions.

- slot `p` stores the current segment sitting there
- step `i` finds the `A_i`-th and `(A_i+1)`-th alive positions
- create their parent
- keep it in the left slot, delete the right slot

This is `O(N log N)`.

## Complexity

- Tree construction: `O(N log N)`
- One target winner (`R`, `P`, or `S`): `O(N)`
- Total per test case: `O(N log N)`

This is fast enough for `sum N <= 2 * 10^5`.
