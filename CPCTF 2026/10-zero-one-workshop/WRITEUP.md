# Zero-One Workshop (CPCTF 2026 ACM)

**Rewrite:** Every effective operation is exactly `01 -> 00` or `01 -> 11`.

**Key cut:** If a pair is initially `10`, it never becomes `01`, so no operation ever crosses that cut. Therefore the string splits independently at every initial `10`.

**Per segment:** Each segment is of the form `0^x1^y`. If `x=0` or `y=0`, nothing can change, so it contributes `1`. If `x,y>0`, the unique `01` boundary can move left or right by one each move, so every `0^k1^(L-k)` with `0<=k<=L` is reachable, where `L=x+y`. That contributes `L+1`.

**Answer:** Split `A` at every initial `10`, and multiply `(segment_length + 1)` over the mixed segments. Take the result modulo `998244353`.

**Examples:** `01 -> 3`, `1111 -> 1`, `0101 -> 3 * 3 = 9`.

**Implementation:** One linear scan. Keep the current segment start, cut when you see `10`, and for each segment multiply by `len+1` iff it contains both `0` and `1`. Total time **O(N)** (each index touched once across segment scans). Checked against samples **1–3** (including `211079167`).

`#include <bits/stdc++.h>` is **g++/Yukicoder**; local **clang** on macOS may need explicit `<iostream>`, `<string>`, etc.

```cpp
// O(N), g++ / Yukicoder
#include <bits/stdc++.h>
using namespace std;

static constexpr long long MOD = 998244353;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    string A;
    cin >> N >> A;

    long long ans = 1;
    int start = 0;

    auto apply_segment = [&](int l, int r) {
        if (l > r) return;
        bool has0 = false, has1 = false;
        for (int i = l; i <= r; ++i) {
            has0 |= (A[i] == '0');
            has1 |= (A[i] == '1');
        }
        if (has0 && has1) {
            ans = ans * (r - l + 2LL) % MOD;
        }
    };

    for (int i = 0; i + 1 < N; ++i) {
        if (A[i] == '1' && A[i + 1] == '0') {
            apply_segment(start, i);
            start = i + 1;
        }
    }
    apply_segment(start, N - 1);

    cout << ans << '\n';
    return 0;
}
```

**Note:** This is the ACM-style task, so there is no separate jeopardy flag here; the goal is just to get AC.
