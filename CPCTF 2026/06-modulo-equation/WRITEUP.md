# Modulo Equation (Yukicoder / CPCTF 2026 PPC)

**Idea:** Find the smallest positive integer \(x\) such that **`x mod A == B mod x`**, with **`A > B`** (constraints roughly **`1 ≤ B < A ≤ 300`**).

**Reasoning:** If **`x > B`**, then **`B mod x = B`**, so you need **`x mod A = B`**, i.e. **`x ≡ B (mod A)`** and **`x > B`**. The smallest such **`x`** is **`A + B`** (first **`B + kA`** with **`k ≥ 1`**). For **`x ≤ B`** you get **`x mod A = x`** (since **`x < A`**) but **`B mod x < x`**, so equality is impossible.

**Solve:** Output **`A + B`**.

**Implementation:** One integer add; e.g. C++: read **`A B`**, print **`A + B`**.

**Contest note:** **AC** on submissions is the coding objective. The **jeopardy-style flag** for this task is **not** in the test ZIP — it’s on the problem **Explanation** tab (same pattern as other CPCTF Yukicoder tasks).

**Flag (from Explanation):** `CPCTF{D1d_y0u_8ru73_f0rc3_17!?}`

**Samples:** `5 3 → 8`, `31 4 → 35`, `202 6 → 208`.
