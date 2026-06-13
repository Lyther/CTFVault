# RangeSum RangeUpdate RangeSqrt (Yukicoder No. 3507)

**Data structure:** Use a segment tree beats variant with `sum`, `mn`, `mx`, plus lazy `assign` and lazy `add`.

**Why `add` is needed even though the queries do not have it:** Let `f(x)=floor(sqrt(x))`. On some intervals, `f(x)` is not constant, but `f(x)-x` is constant. Example: `3 -> 1` and `4 -> 2`, so both values change by `-2`. If a segment satisfies that property for every value inside it, one `sqrt` update is just a range-add by that constant delta.

**Two easy cases for a fully covered node:** Let `a = mn`, `b = mx`, `sa = f(a)`, `sb = f(b)`.

- If `sa == sb`, then every value in the node becomes the same number, so we can lazy-`assign(sa)`.
- If `sa - a == sb - b`, then `g(x)=f(x)-x` has the same endpoint value. Since `g` is nonincreasing, it is constant on `[a,b]`, so we can lazy-`add(sa-a)`.

If neither case holds, recurse to the children.

**Why this is fast:** This is the usual segment-tree-beats amortization. A hard `sqrt` descent only happens when the node cannot be handled by one lazy tag. In that situation the value span `mx-mn` shrinks by at least a constant factor after the update; the troublesome width-`1` boundary cases are exactly what the lazy-`add` shortcut removes. Therefore each node can be hard-descended only `O(log A)` times before becoming easy, and range-assign just resets the node in `O(1)`. Total complexity is `O((N + Q) log N log A)` with `A <= 1e9`, which is easily fast enough.

```cpp
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

using namespace std;

struct SegTree {
    struct Node {
        long long sum = 0;
        int mn = 0;
        int mx = 0;
        long long add = 0;
        bool has_assign = false;
        int assign = 0;
    };

    int n;
    vector<Node> seg;

    explicit SegTree(const vector<int>& a) : n((int)a.size()), seg(4 * n) {
        build(1, 0, n, a);
    }

    static int isqrt_int(int x) {
        int r = (int)std::sqrt((long double)x);
        while (1LL * (r + 1) * (r + 1) <= x) ++r;
        while (1LL * r * r > x) --r;
        return r;
    }

    void build(int idx, int l, int r, const vector<int>& a) {
        if (r - l == 1) {
            seg[idx].sum = a[l];
            seg[idx].mn = a[l];
            seg[idx].mx = a[l];
            return;
        }
        int mid = (l + r) >> 1;
        build(idx << 1, l, mid, a);
        build(idx << 1 | 1, mid, r, a);
        pull(idx);
    }

    void pull(int idx) {
        seg[idx].sum = seg[idx << 1].sum + seg[idx << 1 | 1].sum;
        seg[idx].mn = min(seg[idx << 1].mn, seg[idx << 1 | 1].mn);
        seg[idx].mx = max(seg[idx << 1].mx, seg[idx << 1 | 1].mx);
    }

    void apply_assign(int idx, int l, int r, int v) {
        seg[idx].sum = 1LL * (r - l) * v;
        seg[idx].mn = v;
        seg[idx].mx = v;
        seg[idx].add = 0;
        seg[idx].has_assign = true;
        seg[idx].assign = v;
    }

    void apply_add(int idx, int l, int r, int delta) {
        if (delta == 0) return;
        seg[idx].sum += 1LL * (r - l) * delta;
        seg[idx].mn += delta;
        seg[idx].mx += delta;
        if (seg[idx].has_assign) {
            seg[idx].assign += delta;
        } else {
            seg[idx].add += delta;
        }
    }

    void push(int idx, int l, int r) {
        if (r - l == 1) {
            seg[idx].add = 0;
            seg[idx].has_assign = false;
            return;
        }

        int mid = (l + r) >> 1;
        if (seg[idx].has_assign) {
            apply_assign(idx << 1, l, mid, seg[idx].assign);
            apply_assign(idx << 1 | 1, mid, r, seg[idx].assign);
            seg[idx].has_assign = false;
        }
        if (seg[idx].add != 0) {
            apply_add(idx << 1, l, mid, (int)seg[idx].add);
            apply_add(idx << 1 | 1, mid, r, (int)seg[idx].add);
            seg[idx].add = 0;
        }
    }

    void range_assign(int idx, int l, int r, int ql, int qr, int x) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) {
            apply_assign(idx, l, r, x);
            return;
        }
        push(idx, l, r);
        int mid = (l + r) >> 1;
        range_assign(idx << 1, l, mid, ql, qr, x);
        range_assign(idx << 1 | 1, mid, r, ql, qr, x);
        pull(idx);
    }

    void range_sqrt(int idx, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql || seg[idx].mx <= 1) return;

        if (ql <= l && r <= qr) {
            int sa = isqrt_int(seg[idx].mn);
            int sb = isqrt_int(seg[idx].mx);
            if (sa == sb) {
                apply_assign(idx, l, r, sa);
                return;
            }
            if (sa - seg[idx].mn == sb - seg[idx].mx) {
                apply_add(idx, l, r, sa - seg[idx].mn);
                return;
            }
        }

        if (r - l == 1) {
            apply_assign(idx, l, r, isqrt_int(seg[idx].mx));
            return;
        }

        push(idx, l, r);
        int mid = (l + r) >> 1;
        range_sqrt(idx << 1, l, mid, ql, qr);
        range_sqrt(idx << 1 | 1, mid, r, ql, qr);
        pull(idx);
    }

    long long range_sum(int idx, int l, int r, int ql, int qr) {
        if (qr <= l || r <= ql) return 0;
        if (ql <= l && r <= qr) return seg[idx].sum;
        push(idx, l, r);
        int mid = (l + r) >> 1;
        return range_sum(idx << 1, l, mid, ql, qr)
             + range_sum(idx << 1 | 1, mid, r, ql, qr);
    }

    void range_assign(int l, int r, int x) {
        range_assign(1, 0, n, l, r, x);
    }

    void range_sqrt(int l, int r) {
        range_sqrt(1, 0, n, l, r);
    }

    long long range_sum(int l, int r) {
        return range_sum(1, 0, n, l, r);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, Q;
    cin >> N >> Q;

    vector<int> A(N);
    for (int i = 0; i < N; ++i) cin >> A[i];

    SegTree seg(A);

    for (int qi = 0; qi < Q; ++qi) {
        int type, l, r;
        cin >> type >> l >> r;
        if (type == 0) {
            cout << seg.range_sum(l, r) << '\n';
        } else if (type == 1) {
            int x;
            cin >> x;
            seg.range_assign(l, r, x);
        } else {
            seg.range_sqrt(l, r);
        }
    }
    return 0;
}
```

**Sample:** Start from `[1,2,3,4,5,6]`. Query `0 1 4` gives `2+3+4=9`. After `1 0 3 10`, the array is `[10,10,10,4,5,6]`. After `2 1 3`, it becomes `[10,3,3,4,5,6]`, so `0 1 4` prints `3+3+4=10`.

**Contest note:** This is another ACM-style Yukicoder task in this folder, so the output is just the query answers; there is no separate jeopardy flag.
