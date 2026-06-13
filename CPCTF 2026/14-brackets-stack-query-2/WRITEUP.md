# Brackets Stack Query 2 (Yukicoder No. 3503)

**Definition:** *T* is a **good bar-bracket string** iff you can reach the empty string by repeatedly deleting a contiguous substring equal to `( | )` (three characters).

**Static check:** Scan left to right with a stack: push each character; while the top three are `(` `|` `)` in order, pop them. *T* is good iff the stack is empty. This matches the rewrite system (terminating and confluent for this rule).

**Online:** After `1 c`, append `c` and run the collapse loop. Query `2` removes the **last character of the raw string** *S*, i.e. undoes the **most recent** `1 c` (not “pop one char from the reduced form” without context).

**Undo one `1 c`:** If that append triggered **k** collapses, **reverse** them by **k** times pushing `(` then `|` then `)` (each triple restores one collapse, most recent collapse undone first). Then `pop` once to remove the appended character **c**.

**Output:** After each query, print `Yes` if the stack is empty, else `No`.

**Complexity:** Amortized **O(1)** per character for pushes/collapses under total work **O(Q)**; each undo costs **O(k)** for that query's recorded **k**. Fine for **Q ≤ 8×10^5**.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int Q;
    std::cin >> Q;

    std::vector<char> stk;
    stk.reserve(static_cast<size_t>(Q + 3));

    std::vector<int> collapse_hist;

    auto collapse_all = [&]() {
        int k = 0;
        while (stk.size() >= 3) {
            const size_t n = stk.size();
            if (stk[n - 3] == '(' && stk[n - 2] == '|' && stk[n - 1] == ')') {
                stk.resize(n - 3);
                ++k;
            } else {
                break;
            }
        }
        return k;
    };

    for (int qi = 0; qi < Q; ++qi) {
        int ty;
        std::cin >> ty;
        if (ty == 1) {
            char c;
            std::cin >> c;
            stk.push_back(c);
            collapse_hist.push_back(collapse_all());
        } else {
            int k = collapse_hist.back();
            collapse_hist.pop_back();
            for (int i = 0; i < k; ++i) {
                stk.push_back('(');
                stk.push_back('|');
                stk.push_back(')');
            }
            stk.pop_back();
        }
        std::cout << (stk.empty() ? "Yes" : "No") << '\n';
    }
    return 0;
}
```

**Samples:** After `( | )` the stack is empty → `Yes`. Plain `()` never forms a `( | )` tile → `No`, `No`.

**Contest note:** ACM-style task; no separate jeopardy flag assumed.
