# traQ ID / Sign up for traP (PPC, Yukicoder No. 13201)

The PPC task pays out twice — once for AC, once for finding the hidden CPCTF flag buried in the problem's **Explanation** prose.

## Part A — solve the validation task (AC)

**Idea:** Given one string `S`, decide if it is a valid traQ ID. Print `200` if yes, `400` if no.

**Rules:**

1. **Length** `1 ≤ |S| ≤ 32`.
2. Every character is one of `A–Z`, `a–z`, `0–9`, `_`, `-`.
3. The **first** and **last** character must **not** be `_` or `-`.

**Solve:** Scan `S` once; check length, then charset, then ends. See [main.cpp](main.cpp).

**Local tests:** `13201-testcase/` — `zoi_dayo` → `200`; `CPCTF{dummy}` → `400` (illegal chars); trailing `_` → `400`; single `Z` → `200`; single `-` → `400`.

## Part B — the hidden flag in the Explanation

The flag is **not** in any code or test data. It is embedded in the long Japanese Explanation text that accompanies the yukicoder problem — easy to miss if you only read the formal statement.

**Solve:** Open the problem's Explanation page on Yukicoder and search for `CPCTF{` (or skim the prose).

**Flag:** `CPCTF{s10w1y_bu7_sure1y}`
