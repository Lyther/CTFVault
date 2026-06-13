# I Love DAG (Yukicoder No. 3499, interactive)

**Idea:** Start with an empty graph on **N** vertices. Each step adds **one** directed edge between **A** and **B** (you choose **A→B** → print **`0`**, or **B→A** → print **`1`**). The final graph must stay a **DAG**.

**Solve:** Fix the topological order **1, 2, …, N**. For every query **(A, B)**, always orient **from the smaller label to the larger**:

- if **A < B** → **`0`** (**A → B**);
- else → **`1`** (**B → A**).

Every edge respects the global order **1 < 2 < … < N**, so no directed cycle is possible.

**Implementation:** After each **`cout`**, flush (use **`endl`** or **`cout << flush`**). Complexity **O(M)**.

```cpp
#include <iostream>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) return 0;

    for (int i = 0; i < M; ++i) {
        int A, B;
        cin >> A >> B;
        cout << (A < B ? 0 : 1) << '\n';
        cout.flush();
    }

    return 0;
}
```

**Note:** The official sample uses a different valid orientation; many outputs are accepted. The sample prose listing edges may not match **`0` = A→B / `1` = B→A** on the last line—trust the I/O spec, not the garbled explanation.

**Contest note:** This is the ACM-style task, so there is no separate jeopardy flag here; the goal is just to get AC.
