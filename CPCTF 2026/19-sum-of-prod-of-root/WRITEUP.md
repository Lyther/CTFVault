# Sum of Prod of Root (Yukicoder No. 3505)

**Statement fix:** The sample matches
\[
\sum_{i=1}^{N}\prod_{k=1}^{\infty}\left\lfloor i^{1/k}\right\rfloor
\]
because for \(i=6\) we get \(6\cdot 2=12\). The broken HTML in the statement is just a rendering issue.

Let
\[
F(n)=\prod_{k=1}^{\infty}\left\lfloor n^{1/k}\right\rfloor.
\]
Then
\[
F(n)=n\cdot \lfloor \sqrt n \rfloor \cdot H(n),\qquad
H(n)=\prod_{k=3}^{\infty}\left\lfloor n^{1/k}\right\rfloor.
\]
All but finitely many factors are \(1\), so the product is finite.

**Key observation:** \(H(n)\) changes only when \(n\) is a perfect \(k\)-th power for some \(k\ge 3\). Therefore we do **not** scan square blocks one by one. We only scan the distinct values
\[
x=b^k\le N \quad (b\ge 2,\ k\ge 3).
\]
There are only
\[
\sum_{k\ge 3}\left\lfloor N^{1/k}\right\rfloor = O(N^{1/3})
\]
such generated events, about \(10^6\) even for \(N=10^{18}\).

**What happens at one event:** Suppose \(x=b^k\). When \(n\) increases from \(x-1\) to \(x\), the factor \(\lfloor n^{1/k}\rfloor\) increases from \(b-1\) to \(b\), so \(H\) is multiplied by
\[
\frac{b}{b-1}.
\]
If the same \(x\) has multiple representations, for example \(64=4^3=2^6\), we multiply all corresponding ratios.

So after sorting all distinct perfect powers with exponent at least \(3\), \(H(n)\) is constant on every interval between consecutive events.

**Now only one sum remains:** On an interval \([L,R]\) where \(H\) is constant,
\[
\sum_{n=L}^{R} F(n)=H(L)\sum_{n=L}^{R} n\lfloor \sqrt n\rfloor.
\]
Thus it is enough to compute the prefix sum
\[
W(X)=\sum_{n=1}^{X} n\lfloor \sqrt n\rfloor.
\]

Let \(s=\lfloor \sqrt X\rfloor\). For each full square band \(t^2\le n\le (t+1)^2-1\), \(\lfloor \sqrt n\rfloor=t\), so
\[
W(X)
=\sum_{t=1}^{s-1} t\sum_{n=t^2}^{(t+1)^2-1} n
 \;+\;
s\sum_{n=s^2}^{X} n.
\]
The inner full-band sum is
\[
\sum_{n=t^2}^{(t+1)^2-1} n
= t(t+1)(2t+1),
\]
so
\[
t\sum_{n=t^2}^{(t+1)^2-1} n
= t^2(t+1)(2t+1)
= 2t^4+3t^3+t^2.
\]
Therefore
\[
W(X)=
2\sum_{t=1}^{s-1} t^4
+3\sum_{t=1}^{s-1} t^3
+\sum_{t=1}^{s-1} t^2
+s\left(\sum_{n=1}^{X}n-\sum_{n=1}^{s^2-1}n\right),
\]
and every term has a standard closed form modulo \(998244353\).

**Algorithm:**

1. Enumerate every pair \((b,k)\) with \(k\ge 3\) and \(b^k\le N\).
2. For each event \(x=b^k\), attach multiplier \(b/(b-1)\pmod{998244353}\).
3. Sort by \(x\) and merge equal values by multiplying their ratios.
4. Sweep the event list. If the current interval is \([cur, x-1]\), add
   \[
   H\cdot (W(x-1)-W(cur-1)).
   \]
5. Apply the merged multiplier at \(x\), then continue.
6. Finally add the tail interval after the last event.

**Complexity:** Event generation is
\[
O\!\left(\sum_{k\ge 3} N^{1/k}\right)=O(N^{1/3}),
\]
sorting is \(O(M\log M)\) for \(M=O(N^{1/3})\), and the sweep is linear. This easily fits \(N\le 10^{18}\).

```cpp
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

using namespace std;

using int64 = long long;
using i128 = __int128_t;

static constexpr int64 MOD = 998244353;
static constexpr int64 INV2 = (MOD + 1) / 2;
static constexpr int64 INV6 = 166374059;   // 6^{-1} mod MOD
static constexpr int64 INV30 = 432572553;  // 30^{-1} mod MOD

int64 mul_mod(int64 a, int64 b) {
    return (i128)a * b % MOD;
}

int64 add_mod(int64 a, int64 b) {
    a += b;
    if (a >= MOD) a -= MOD;
    return a;
}

int64 sub_mod(int64 a, int64 b) {
    a -= b;
    if (a < 0) a += MOD;
    return a;
}

bool le_pow(int64 base, int k, int64 limit) {
    i128 cur = 1;
    for (int i = 0; i < k; ++i) {
        cur *= base;
        if (cur > limit) return false;
    }
    return true;
}

int64 kth_root_floor(int64 n, int k) {
    if (k == 1 || n <= 1) return n;
    long double x = pow((long double)n, 1.0L / k);
    int64 r = (int64)x;
    if (r < 1) r = 1;
    while (le_pow(r + 1, k, n)) ++r;
    while (!le_pow(r, k, n)) --r;
    return r;
}

int64 isqrt_floor(int64 n) {
    int64 r = (int64)sqrt((long double)n);
    while ((i128)(r + 1) * (r + 1) <= n) ++r;
    while ((i128)r * r > n) --r;
    return r;
}

int64 tri(int64 n) {
    if (n <= 0) return 0;
    return mul_mod(mul_mod(n % MOD, (n + 1) % MOD), INV2);
}

int64 sum2(int64 n) {
    if (n <= 0) return 0;
    int64 a = n % MOD;
    int64 b = (n + 1) % MOD;
    int64 c = (2 * (n % MOD) + 1) % MOD;
    return mul_mod(mul_mod(a, b), mul_mod(c, INV6));
}

int64 sum3(int64 n) {
    if (n <= 0) return 0;
    int64 t = tri(n);
    return mul_mod(t, t);
}

int64 sum4(int64 n) {
    if (n <= 0) return 0;
    int64 a = n % MOD;
    int64 b = (n + 1) % MOD;
    int64 c = (2 * (n % MOD) + 1) % MOD;
    int64 d = (3 * mul_mod(a, a) + 3 * a - 1) % MOD;
    if (d < 0) d += MOD;
    return mul_mod(mul_mod(mul_mod(a, b), c), mul_mod(d, INV30));
}

// W(x) = sum_{n=1}^{x} n * floor(sqrt(n))
int64 prefix_weight(int64 x) {
    if (x <= 0) return 0;

    int64 s = isqrt_floor(x);
    int64 m = s - 1;

    int64 full = 0;
    full = add_mod(full, mul_mod(2, sum4(m)));
    full = add_mod(full, mul_mod(3, sum3(m)));
    full = add_mod(full, sum2(m));

    int64 tail = mul_mod(s % MOD, sub_mod(tri(x), tri((int64)((i128)s * s - 1))));
    return add_mod(full, tail);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int64 N;
    cin >> N;

    int64 max_base = kth_root_floor(N, 3);
    vector<int64> inv(max<int64>(max_base + 1, 2), 1);
    for (int64 i = 2; i <= max_base; ++i) {
        inv[i] = MOD - mul_mod(MOD / i, inv[MOD % i]);
    }

    vector<pair<int64, int64>> events;
    for (int k = 3; k <= 60; ++k) {
        int64 lim = kth_root_floor(N, k);
        for (int64 b = 2; b <= lim; ++b) {
            i128 p = 1;
            for (int i = 0; i < k; ++i) p *= b;
            events.push_back({(int64)p, mul_mod(b % MOD, inv[b - 1])});
        }
    }

    sort(events.begin(), events.end());

    vector<pair<int64, int64>> merged;
    merged.reserve(events.size());
    for (auto [x, mul] : events) {
        if (!merged.empty() && merged.back().first == x) {
            merged.back().second = mul_mod(merged.back().second, mul);
        } else {
            merged.push_back({x, mul});
        }
    }

    int64 ans = 0;
    int64 cur = 1;
    int64 h = 1;  // current value of H(n) on the active interval

    for (auto [x, mul] : merged) {
        if (cur <= x - 1) {
            int64 segment = sub_mod(prefix_weight(x - 1), prefix_weight(cur - 1));
            ans = add_mod(ans, mul_mod(h, segment));
        }
        h = mul_mod(h, mul);
        cur = x;
    }

    if (cur <= N) {
        int64 segment = sub_mod(prefix_weight(N), prefix_weight(cur - 1));
        ans = add_mod(ans, mul_mod(h, segment));
    }

    cout << ans << '\n';
    return 0;
}
```

**Sample:** For \(N=6\),
\[
F(1),F(2),F(3),F(4),F(5),F(6)=1,2,3,8,10,12,
\]
so the answer is \(1+2+3+8+10+12=36\).

**Contest note:** ACM-style task, so the output is just the single numeric answer.
