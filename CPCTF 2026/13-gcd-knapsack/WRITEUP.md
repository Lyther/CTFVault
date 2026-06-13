# GCD Knapsack (Yukicoder No. 3502)

**Idea:** A chosen set is valid iff the gcd of its weights is at least `W`. That means there exists some integer `d >= W` dividing every chosen weight. Since every value `Y[i]` is positive, for a fixed `d` the best choice is simply **all** items whose weights are multiples of `d`.

**Reformulation:** For each `d >= W`, let `S[d] = sum of Y[i] over all items with d | X[i]`. Then the answer is `max S[d]`. If no item can be chosen, every `S[d]` is `0`, so the answer is `0`.

**Why this is enough:** If a subset has gcd `g >= W`, then every selected weight is a multiple of `g`, so its total value is at most `S[g]`. Conversely, if we take **all** items whose weights are multiples of some `d >= W`, then every chosen weight is divisible by `d`, so their gcd is also divisible by `d`, hence at least `d >= W`. Therefore `S[d]` itself is always achievable, and the answer is exactly `max_{d >= W} S[d]`.

**Implementation:** Accumulate `sum_exact[x] = total value of items with weight exactly x`. Then for each `d`, sum `sum_exact[d] + sum_exact[2d] + sum_exact[3d] + ...`. This is `O(M log M)` for `M = max(X[i])`, which fits `2e5`.

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, W;
    cin >> N >> W;

    vector<int> X(N);
    int max_x = 0;
    for (int i = 0; i < N; ++i) {
        cin >> X[i];
        if (X[i] > max_x) max_x = X[i];
    }

    vector<long long> sum_exact(max_x + 1, 0);
    for (int i = 0; i < N; ++i) {
        long long y;
        cin >> y;
        sum_exact[X[i]] += y;
    }

    long long ans = 0;
    for (int d = W; d <= max_x; ++d) {
        long long cur = 0;
        for (int multiple = d; multiple <= max_x; multiple += d) {
            cur += sum_exact[multiple];
        }
        if (cur > ans) ans = cur;
    }

    cout << ans << '\n';
    return 0;
}
```

**Examples:** In sample 1, `d=2` gives value `5+2=7`, `d=3` gives `8`, `d=4` gives `5`, so the answer is `8`. If every `X[i] < W`, no singleton works either, so the answer is immediately `0`.

**Contest note:** This is the ACM-style task, so there is no separate jeopardy flag here; the goal is just to get AC.
