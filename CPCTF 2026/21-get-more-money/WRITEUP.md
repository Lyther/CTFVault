# Get More Money (Yukicoder / CPCTF 2026 PPC)

**Setting:** Over `N` days, Alice can buy up to `B_i` jewels at price `A_i`, sell up to `D_i` jewels at price `C_i`, and carry at most `K` jewels into the next day. Maximise total profit after day `N`.

**Key observation:** On day `i`, the "contribution" of each held jewel to its final sale is `(day-i sell price) − (purchase price)`. We never want to sell at a loss, and we always want to sell the cheapest-purchased jewels first. At the end of day `i` we also must drop the cheapest jewels whose total count exceeds `K` (they "don't fit in the vault").

**Strategy:** keep a bag of jewels the owner is currently holding, each annotated with purchase price. On day `i`:

1. Add `B_i` virtual jewels at price `A_i` to the bag (available for sale today or later).
2. While the bag is non-empty and we have sale-quota `D_i` left, pick the jewel in the bag with the **lowest purchase price** (since we'll pocket the biggest margin `C_i − A`). Stop once the top margin would be non-positive — we prefer holding to selling at a loss.
3. When we sell a jewel, re-insert one at price `C_i`. This represents the fact that *we could have bought it today at `A_i` instead, sold at `C_i`, and carried the difference as pure profit*; alternatively, if later days have even higher sell prices, we can "buy back" this virtual slot at cost `C_i` and sell at the better price. This bookkeeping trick makes greedy correct.
4. After today's trading, drop the cheapest jewels until the bag fits in `K`.

Use a `map<int64_t, int64_t>` keyed by **negated purchase price** so `prev(end())` gives the smallest-cost jewel (for selling) and `begin()` gives the largest-cost jewel (for discarding).

Profit may overflow 64-bit, so accumulate in `__int128` and print with a custom printer.

## Complexity

Each jewel enters and leaves the map at most O(1) times amortised, so each test case is `O(N log N)`; total `O(sum(N) · log N)` which fits in the `sum(N) ≤ 2·10^5` constraint.

## Reference

The provided [main.cpp](main.cpp) is already the intended solution — it implements exactly the above strategy with a `std::map<i64, i64>` and `__int128` accumulator.
