# Digit Products 2 (Yukicoder No. 3501, interactive)

**Idea:** Query the most significant digit, not the ones digit. Let the digits be `d[0],...,d[N-1]` with `d[N-1] != 0`. Ask `? i N-1` for every `0 <= i < N-1`, so `q[i] = d[i] * d[N-1]`.

**Case 1:** If at least two `q[i]` are positive, say `q[a] > 0` and `q[b] > 0`, ask one more query `? a b` and get `r = d[a] * d[b]`. Then `q[a] * q[b] = r * d[N-1]^2`, so the top digit is fixed, and every other digit is `d[i] = q[i] / d[N-1]`. Thus the whole number is uniquely determined within exactly `N` queries.

**Case 2:** If no `q[i]` is positive, the MS digit is the only nonzero digit. Every possible query returns `0`, so numbers like `1000...0`, `2000...0`, ..., `9000...0` are indistinguishable. Output `! -1`.

**Case 3:** If exactly one `q[k]` is positive, then only positions `k` and `N-1` are nonzero. Any query except `{k, N-1}` returns `0`, and `{k, N-1}` only reveals the product `d[k] * d[N-1]`. So the instance is solvable iff that product has exactly one ordered factor pair in `[1,9]^2`; otherwise output `! -1`. Examples: `25 -> (5,5)` is unique, `2 -> (1,2)` or `(2,1)` is not.

**Implementation:** Build the answer as a string because `N` can be `51`. After every query or final answer, flush. If the judge returns `-1`, exit immediately.

```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static void answer(const string& s) {
    cout << "! " << s << '\n';
    cout.flush();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<int> q(N - 1);
    for (int i = 0; i < N - 1; ++i) {
        cout << "? " << i << ' ' << N - 1 << '\n';
        cout.flush();
        cin >> q[i];
        if (q[i] == -1) return 0;
    }

    vector<int> pos;
    for (int i = 0; i < N - 1; ++i) {
        if (q[i] > 0) pos.push_back(i);
    }

    auto make_string = [&](const vector<int>& d) {
        string s;
        s.reserve(N);
        for (int i = N - 1; i >= 0; --i) s.push_back(char('0' + d[i]));
        return s;
    };

    if (pos.empty()) {
        answer("-1");
        return 0;
    }

    if (pos.size() == 1) {
        int k = pos[0];
        int prod = q[k];
        string only;
        int cnt = 0;
        for (int low = 1; low <= 9; ++low) {
            for (int high = 1; high <= 9; ++high) {
                if (low * high != prod) continue;
                vector<int> d(N, 0);
                d[k] = low;
                d[N - 1] = high;
                only = make_string(d);
                ++cnt;
            }
        }
        if (cnt == 1) answer(only);
        else answer("-1");
        return 0;
    }

    int a = pos[0];
    int b = pos[1];
    cout << "? " << a << ' ' << b << '\n';
    cout.flush();

    int r;
    cin >> r;
    if (r == -1) return 0;

    string only;
    int cnt = 0;
    for (int top = 1; top <= 9; ++top) {
        if (q[a] * q[b] != top * top * r) continue;
        vector<int> d(N, 0);
        d[N - 1] = top;
        bool ok = true;
        for (int i = 0; i < N - 1; ++i) {
            if (q[i] % top != 0) {
                ok = false;
                break;
            }
            d[i] = q[i] / top;
            if (d[i] < 0 || d[i] > 9) {
                ok = false;
                break;
            }
        }
        if (!ok) continue;
        only = make_string(d);
        ++cnt;
    }

    if (cnt == 1) answer(only);
    else answer("-1");
    return 0;
}
```

**Examples:** `201` is impossible because only digits `2` and `1` are nonzero and product `2` does not fix their order. `5005` is solvable because the only positive product is `25`, which forces `(5,5)`. `1230` is solvable: query the MS digit `1`, not the ones digit `0`.

**Contest note:** This is the ACM-style task, so there is no separate jeopardy flag here; the goal is just to get AC.
